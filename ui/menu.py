import pygame
from settings import WIDTH, HEIGHT, WHITE

class Menu:
    def __init__(self, font):
        self.font = font

    def draw_start(self, screen):
        text = self.font.render("Press SPACE to Start", True, WHITE)
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2))