import pygame
import random

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2,5)
        self.dx = random.uniform(-2,2)
        self.dy = random.uniform(-2,2)
        self.life = 30

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, (255,200,0), (int(self.x), int(self.y)), self.size)