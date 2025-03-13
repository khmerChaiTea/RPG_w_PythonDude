import pygame

class AllSprites(pygame.sprite.LayeredUpdates):
    """Custom sprite group that supports layers."""
    
    def __init__(self):
        super().__init__()

    def update(self, *args):
        """Override update to apply any custom logic, if needed."""
        super().update(*args)

    def add_sprite(self, sprite, layer=0):
        """Adds a sprite to a specific layer."""
        self.add(sprite, layer=layer)
