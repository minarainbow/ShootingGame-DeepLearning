import random
import pygame

pad_width = 1200
pad_height = 600

class Fire():
    def __init__(self, filename, height):
        self.x = pad_width
        self.y = random.randrange(0, pad_height - height)
        self.height = height
        self.image = pygame.image.load('game/images/fireball.png')

    def draw(self, gamepad):
        gamepad.blit(self.image, (self.x, self.y))
