import pygame, random
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
        self.image = game.terrain_spritesheet.get_image(991, 542, TILESIZE, TILESIZE)  # Different tile for block
        self.rect = self.image.get_rect(topleft=(x * TILESIZE, y * TILESIZE))
        
class Player(pygame.sprite.Sprite): 
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)  # Add to all_sprites group
        game.player_group.add(self)  # Add player separately
        
        self.game = game
        self.image = game.player_spritesheet.get_image(0, 0, TILESIZE, TILESIZE)
        self.rect = self.image.get_rect(topleft=(x * TILESIZE, y * TILESIZE))
        
        # Movement attributes
        self.x_change = 0
        self.y_change = 0
        
        self.direction = "down"
        
    def update(self):
        self.move()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        
        self.x_change = 0
        self.y_change = 0
        
    def move(self):
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.x_change = -PLAYER_STEPS
            self.direction = "left"
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.x_change = PLAYER_STEPS
            self.direction = "right"            
        elif pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.y_change = -PLAYER_STEPS
            self.direction = "up"   
        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.y_change = PLAYER_STEPS
            self.direction = "down"
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites, game.enemies)  # Add to all_sprites and enemies group
        
        self.game = game
        self.image = game.enemy_spritesheet.get_image(0, 0, TILESIZE, TILESIZE)
        self.rect = self.image.get_rect(topleft=(x * TILESIZE, y * TILESIZE))
        
        # Movement attributes
        self.x_change = 0
        self.y_change = 0
        
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.numberSteps = random.choice([30, 40, 50, 60, 70, 80, 90])
        self.stallSteps = 120
        self.currentSteps = 0
        
        self.state = "moving"
        
    def update(self):
        self.move()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        
        self.x_change = 0
        self.y_change = 0
        if self.currentSteps == self.numberSteps:
            if self.state != "stalling":
                self.currentSteps = 0
                
            self.direction = random.choice(['left', 'right', 'up', 'down'])
            self.state = "stalling"
            
        
    def move(self):
        
        if self.state == "moving":
            
            if self.direction == "left":
                self.x_change = self.x_change - ENEMY_STEPS
                self.currentSteps += 1
                
            if self.direction == "right":
                self.x_change = self.x_change + ENEMY_STEPS
                self.currentSteps += 1
                
            if self.direction == "up":
                self.y_change = self.y_change - ENEMY_STEPS
                self.currentSteps += 1
                
            if self.direction == "down":
                self.y_change = self.y_change + ENEMY_STEPS
                self.currentSteps += 1
                
        elif self.state == "stalling":
            
            self.currentSteps += 1
            if self.currentSteps == self.stallSteps:
                self.state = "moving"
                self.currentSteps = 0
            