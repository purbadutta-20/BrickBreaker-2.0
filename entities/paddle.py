import pygame
from settings import WIDTH, BLUE

class Paddle:
    def __init__(self):
        self.width = 120
        self.height = 15
        self.rect = pygame.Rect(WIDTH//2 - 60, 550, self.width, self.height)
        self.speed = 8

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect, border_radius=8)