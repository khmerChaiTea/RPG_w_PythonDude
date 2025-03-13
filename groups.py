import pygame

class AllSprites(pygame.sprite.Group):
    """Custom sprite group for handling all sprites."""
    def __init__(self):
        super().__init__()

    def draw(self, screen):
        """Override draw to handle all sprite layers (optional)."""
        super().draw(screen)

    def update(self, *args):
        """Override update to apply any custom update logic."""
        super().update(*args)
