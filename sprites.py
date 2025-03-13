import pygame
from settings import *
from groups import AllSprites

class Spritesheet:
    """Loads and extracts images from a spritesheet."""
    def __init__(self, path):
        self.spritesheet = pygame.image.load(path).convert()

    def get_image(self, x, y, width, height):
        """Extracts a single sprite from the spritesheet."""
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)  # Add to the main sprite group
        self.image = game.terrain_spritesheet.get_image(447, 353, TILESIZE, TILESIZE)
        self.rect = self.image.get_rect(topleft=(x * TILESIZE, y * TILESIZE))

class Block(Ground):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = game.terrain_spritesheet.get_image(991, 541, TILESIZE, TILESIZE)  # Different tile for block
        self.rect = self.image.get_rect(topleft=(x * TILESIZE, y * TILESIZE))