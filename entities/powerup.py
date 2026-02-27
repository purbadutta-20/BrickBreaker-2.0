import pygame
from settings import HEIGHT, YELLOW

class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = 4

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)

    def off_screen(self):
        return self.rect.top > HEIGHT