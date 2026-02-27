import pygame
import random
from settings import WIDTH, HEIGHT, RED

class Ball:
    def __init__(self):
        self.radius = 10
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(WIDTH//2, HEIGHT//2, 20, 20)
        self.dx = random.choice([-4,4])
        self.dy = -4

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1
        if self.rect.top <= 0:
            self.dy *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, RED, self.rect)