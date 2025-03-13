import pygame
from settings import *

class Block(pygame.sprite.Sprite):
    def __init__(self, groups, x, y):
        super().__init__(groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
