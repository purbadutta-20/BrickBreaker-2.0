import pygame

def load_sounds():
    bounce = pygame.mixer.Sound("assets/bounce.wav")
    brick = pygame.mixer.Sound("assets/brick.wav")
    power = pygame.mixer.Sound("assets/powerup.wav")
    bounce.set_volume(0.3)
    brick.set_volume(0.5)
    power.set_volume(0.6)
    return bounce, brick, power

def play_music():
    pygame.mixer.music.load("assets/bg_music.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    