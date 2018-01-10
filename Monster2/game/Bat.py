import random
import pygame

pad_width = 1200
pad_height = 600

class Bat():
    def __init__(self):
        self.x = pad_width
        self.y = random.randrange(0, pad_height - 70)
        self.image = pygame.image.load('game/images/bat.png')
        self.isShot = False

    def draw(self, gamepad):
        gamepad.blit(self.image, (self.x, self.y))
