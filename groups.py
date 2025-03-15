import pygame

class AllSprites(pygame.sprite.LayeredUpdates):
    """Custom sprite group that supports layers."""
    
    def __init__(self):
        super().__init__()