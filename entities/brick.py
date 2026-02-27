import pygame
from settings import GREEN, YELLOW

class Brick:
    def __init__(self, x, y, strength=1):
        self.rect = pygame.Rect(x, y, 90, 30)
        self.strength = strength

    def hit(self):
        self.strength -= 1

    def draw(self, screen):
        color = GREEN if self.strength == 1 else YELLOW
        pygame.draw.rect(screen, color, self.rect, border_radius=6)