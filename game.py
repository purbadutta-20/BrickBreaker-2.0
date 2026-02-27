import pygame
import sys
import random

from settings import *
from entities.paddle import Paddle
from entities.ball import Ball
from entities.brick import Brick
from entities.powerup import PowerUp
from utils.storage import load_high_score, save_high_score
from utils.sound import load_sounds, play_music
from ui.menu import Menu
from ui.hud import draw_hud

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(-3, 3)
        self.life = random.randint(20, 40)
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.size)
        
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Brick Breaker")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.big_font = pygame.font.SysFont("arial", 60)

        # Sounds
        self.bounce_sound, self.brick_sound, self.power_sound = load_sounds()
        play_music()

        
        self.running = True
        self.state = "start"
         #combo system
        self.combo = 0
        self.combo_timer = 0
        self.multiplier = 1
        
         # Difficulty
        self.difficulty = "medium"
        
        #Particles
        self.particles = []
        
        #Animation timer
        self.game_over_timer = 0

        # Load High Score
        self.high_score = load_high_score()

        self.reset_game()

        self.menu = Menu(self.big_font)

   
    # RESET GAME
    
    def reset_game(self):
        self.paddle = Paddle()
        self.ball = Ball()
        # Difficulty setup
        if self.difficulty =="easy":
            self.lives = 5
            self.ball.dx *= 0.8
            self.ball.dy *= 0.8
            
        elif self.difficulty == "medium":
            self.lives = 3
            
        elif self.difficulty == "hard":
            self.lives = 2
            self.ball.dx *= 1.3
            self.ball.dy *= 1.3
            
        self.level = 1
        self.lives = 3
        self.score = 0
        self.powerups = []
        
        self.combo = 0
        self.multiplier = 1
        
        self.create_level()

   
    # CREATE LEVEL
    def create_level(self):
        self.bricks = []
        rows = 3 + self.level
        cols = 8

        for row in range(rows):
            for col in range(cols):
                x = col * 100 + 50
                y = row * 40 + 60
                strength = 1 if row < 2 else 2
                self.bricks.append(Brick(x, y, strength))

   
    # COLLISIONS
    def handle_collisions(self):
        # Paddle collision
        if self.ball.rect.colliderect(self.paddle.rect):
            self.combo = 0
            self.multiplier = 1
            self.ball.dy *= -1
            self.bounce_sound.play()

        # Brick collision
        for brick in self.bricks[:]:
            if self.ball.rect.colliderect(brick.rect):
                brick.hit()
                self.ball.dy *= -1
               
                self.brick_sound.play()

                # Drop power-up randomly
                if random.random() < 0.2:
                    self.powerups.append(PowerUp(brick.rect.x, brick.rect.y))

               
                if brick.strength <= 0:

                    # Combo system
                    self.combo += 1
                    self.multiplier = 1 + (self.combo // 5)
                    self.score += 10 * self.multiplier

                    # Particle effect
                    for _ in range(10):
                     self.particles.append(
                     Particle(brick.rect.centerx, brick.rect.centery)
                     )

                    self.bricks.remove(brick)
                    break

        # Ball falls
        if self.ball.rect.bottom >= HEIGHT:
            self.lives -= 1
            self.ball.reset()
            self.paddle = Paddle()

    
    # UPDATE POWERUPS
    
    def update_powerups(self):
        for power in self.powerups[:]:
            power.update()

            if power.rect.colliderect(self.paddle.rect):
                self.power_sound.play()
                self.paddle.width += 30
                self.paddle.rect.width = self.paddle.width
                self.powerups.remove(power)

            elif power.off_screen():
                self.powerups.remove(power)

   
    # LEVEL PROGRESSION
    
    def check_level_complete(self):
        if not self.bricks:
            self.level += 1
            self.ball.dx *= 1.2
            self.ball.dy *= 1.2
            self.create_level()
    def update_particles(self):
       for p in self.particles[:]:
           p.update()
           if p.life <= 0:
              self.particles.remove(p)
   
    # GAME LOOP
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_high_score(self.high_score)
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_SPACE:
                         self.state = "playing"

                    if event.key == pygame.K_1:
                       self.difficulty = "easy"

                    if event.key == pygame.K_2:
                          self.difficulty = "medium"

                    if event.key == pygame.K_3:
                       self.difficulty = "hard"

                    if event.key == pygame.K_p and self.state == "playing":
                          self.state = "paused"

                    elif event.key == pygame.K_p and self.state == "paused":
                           self.state = "playing"

                    if event.key == pygame.K_p:
                        self.paused = not self.paused

                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.game_active = True

            
            if self.state == "start":
                 self.menu.draw_start(self.screen)

                 difficulty_text = self.font.render(
                    f"Difficulty: {self.difficulty}", True, WHITE
                 )
                 self.screen.blit(difficulty_text, (WIDTH//2 - 100, HEIGHT//2 + 100))

                 pygame.display.flip()
                 continue
                 

            if self.state == "paused":
                pause_text = self.big_font.render("PAUSED", True, WHITE)
                self.screen.blit(pause_text, (WIDTH//2 - 120, HEIGHT//2))
                pygame.display.flip()
                continue

            # Update
            keys = pygame.key.get_pressed()
            self.paddle.update(keys)
            self.ball.update()

            self.handle_collisions()
            self.update_powerups()
            self.check_level_complete()

            # Update High Score
            if self.score > self.high_score:
                self.high_score = self.score

            # Draw
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)

            for brick in self.bricks:
                brick.draw(self.screen)
            for p in self.particles:
                 p.draw(self.screen)
                 
            for power in self.powerups:
                power.draw(self.screen)

            draw_hud(self.screen, self.font, self.score, self.lives, self.level, self.high_score)

            # Game Over
            
            if self.lives <= 0:
              self.state = "gameover"
              self.game_over_timer = pygame.time.get_ticks()
              if self.state == "gameover":

                 elapsed = pygame.time.get_ticks() - self.game_over_timer

                 size = 60 + int(10 * pygame.math.sin(elapsed * 0.01))
                 font = pygame.font.SysFont("arial", size)

                 text = font.render("GAME OVER", True, RED)
                 self.screen.blit(text, (WIDTH//2 - 180, HEIGHT//2))

                 if elapsed > 3000:
                     save_high_score(self.high_score)
                     self.reset_game()
                     self.state = "start"

            pygame.display.flip()