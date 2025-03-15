import math
import pygame, random
from settings import *
from pygame.sprite import LayeredUpdates

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
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = game.terrain_spritesheet.get_image(447, 352, self.width, self.height)
        self.rect = self.image.get_rect(topleft=(x * self.width, y * self.height))

class Block(Ground):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = game.terrain_spritesheet.get_image(991, 542, self.width, self.height)  # Different tile for block
        self.rect = self.image.get_rect(topleft=(x * self.width, y * self.height))
        
class Player(pygame.sprite.Sprite): 
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)  # Add to all_sprites group
        game.player_group.add(self)  # Add player separately
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.game = game
        self.image = game.player_spritesheet.get_image(0, 0, self.width, self.height)
        self.rect = self.image.get_rect(topleft=(x * self.width, y * self.height))
        self.hitbox_rect = self.rect.copy()
        
        # Movement attributes
        self.direction = pygame.math.Vector2(0, 0)  # Movement vector (x, y)
        self.current_direction = "down"  # Track the current direction for animation
        
        self.animation_counter = 0
        self.collision_sprites = game.blocks  # Use the game's block group
        
        # Animation frames for each direction
        self.animations = {
            "down": [
                self.game.player_spritesheet.get_image(0, 0, self.width, self.height),
                self.game.player_spritesheet.get_image(32, 0, self.width, self.height),
                self.game.player_spritesheet.get_image(64, 0, self.width, self.height)
            ],
            "left": [
                self.game.player_spritesheet.get_image(0, 32, self.width, self.height),
                self.game.player_spritesheet.get_image(32, 32, self.width, self.height),
                self.game.player_spritesheet.get_image(64, 32, self.width, self.height)
            ],
            "right": [
                self.game.player_spritesheet.get_image(0, 64, self.width, self.height),
                self.game.player_spritesheet.get_image(32, 64, self.width, self.height),
                self.game.player_spritesheet.get_image(64, 64, self.width, self.height)
            ],
            "up": [
                self.game.player_spritesheet.get_image(0, 96, self.width, self.height),
                self.game.player_spritesheet.get_image(32, 96, self.width, self.height),
                self.game.player_spritesheet.get_image(64, 96, self.width, self.height)
            ]
        }
        
    def move(self, dt):
        pressed = pygame.key.get_pressed()  # Get current state of all keys

        # Reset direction
        self.direction.x = 0
        self.direction.y = 0

        # Detect movement based on key presses
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.direction.x = -PLAYER_STEPS * dt
            self.current_direction = "left"
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.direction.x = PLAYER_STEPS * dt
            self.current_direction = "right"            
        elif pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.direction.y = -PLAYER_STEPS * dt
            self.current_direction = "up"   
        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.direction.y = PLAYER_STEPS * dt
            self.current_direction = "down"

    def update(self, dt):
        # Step 1: Handle player movement (first)
        self.move(dt)  # Update movement based on key press
        
        # Step 2: Check for collisions with blocks (before updating the position)
        self.hitbox_rect.x += round(self.direction.x)
        self.collide_block("horizontal")  # Collide in horizontal direction
        
        self.hitbox_rect.y += round(self.direction.y)
        self.collide_block("vertical")   # Collide in vertical direction
        
        # Step 3: Update player rect position after handling collisions
        self.rect.topleft = self.hitbox_rect.topleft  # Update sprite position
        
        # Step 4: Animate the player if moving
        self.animation()
            
    def animation(self):
        # Check if the player is moving (has a non-zero direction)
        if self.direction.x != 0 or self.direction.y != 0:
            animation = self.animations[self.current_direction]
            self.image = animation[int(self.animation_counter)]
            self.animation_counter += 0.2  # Increment animation frame counter when moving
            
            if self.animation_counter >= len(animation):
                self.animation_counter = 0
        else:
            # When no movement, keep the player in the current frame
            self.animation_counter = 0  # Optionally reset to the first frame
            self.image = self.animations[self.current_direction][0]  # Show the first frame of the current direction

    def collide_block(self, direction):
        for sprite in self.collision_sprites:
            if self.hitbox_rect.colliderect(sprite.rect):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left  # Prevent movement to the right
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right  # Prevent movement to the left

                if direction == "vertical":
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top  # Prevent movement downward
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom  # Prevent movement upward
                        self.direction.y = 0  # Stop vertical movement after collision
                   
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites, game.enemies)  
        self.width = TILESIZE
        self.height = TILESIZE        
        
        self.game = game
        self.image = game.enemy_spritesheet.get_image(0, 0, self.width, self.height)
        self.rect = self.image.get_rect(topleft=(x * self.width, y * self.height))

        self.x_change = 0
        self.y_change = 0
        self.animation_counter = 1
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.state = "moving"
        self.number_steps = random.choice([30, 40, 50, 60, 70, 80, 90])
        self.stall_steps = 120  # Regular stalling steps
        self.current_steps = 0
        self.collision_reacting_steps = 30  # Reacting steps when colliding
        self.collision_reaction_counter = 0  # Initialize counter for tracking reaction time after collision
        
        self.moving = False  # Default to not moving
        
        # Animation frames for each direction
        self.animations = {
            "down": [
                self.game.enemy_spritesheet.get_image(0, 0, self.width, self.height),
                self.game.enemy_spritesheet.get_image(32, 0, self.width, self.height),
                self.game.enemy_spritesheet.get_image(64, 0, self.width, self.height)
            ],
            "left": [
                self.game.enemy_spritesheet.get_image(0, 32, self.width, self.height),
                self.game.enemy_spritesheet.get_image(32, 32, self.width, self.height),
                self.game.enemy_spritesheet.get_image(64, 32, self.width, self.height)
            ],
            "right": [
                self.game.enemy_spritesheet.get_image(0, 64, self.width, self.height),
                self.game.enemy_spritesheet.get_image(32, 64, self.width, self.height),
                self.game.enemy_spritesheet.get_image(64, 64, self.width, self.height)
            ],
            "up": [
                self.game.enemy_spritesheet.get_image(0, 96, self.width, self.height),
                self.game.enemy_spritesheet.get_image(32, 96, self.width, self.height),
                self.game.enemy_spritesheet.get_image(64, 96, self.width, self.height)
            ]
        }

    def move(self, dt):
        if self.state == "moving":
            if self.direction == "left":
                self.x_change -= ENEMY_STEPS * dt
            elif self.direction == "right":
                self.x_change += ENEMY_STEPS * dt
            elif self.direction == "up":
                self.y_change -= ENEMY_STEPS * dt
            elif self.direction == "down":
                self.y_change += ENEMY_STEPS * dt
            self.current_steps += 1

        elif self.state == "stalling":
            self.current_steps += 1
            if self.current_steps == self.stall_steps:
                self.state = "moving"
                self.current_steps = 0
                self.direction = random.choice(['left', 'right', 'up', 'down'])
                
        elif self.state == "collision_reacting":
            self.collision_reaction_counter += 1
            if self.collision_reaction_counter >= self.collision_reacting_steps:
                self.state = "moving"  # After reaction, start moving again
                self.current_steps = 0
                     
    def update(self, dt):
        self.moving = self.state == "moving"  # Ensure animation plays when moving
        
        # If the enemy is colliding, stop animation
        if self.state == "collision_reacting":
            self.animation_counter = 0  # Stop animation at current frame
        
        self.move(dt)
        self.animation()

        # Step 1: Move and check for collision with blocks (horizontal first)
        self.rect.x += self.x_change
        self.collide_block("horizontal")  # Handle collision in the horizontal direction
        
        # Step 2: Move and check for collision with blocks (vertical)
        self.rect.y += self.y_change
        self.collide_block("vertical")  # Handle collision in the vertical direction
        
        # Step 3: Reset movement after checking collision
        self.x_change = 0
        self.y_change = 0
        
        # If the enemy is moving again, resume animation
        if self.state != "collision_reacting":
            self.animation_counter += 1

        if self.current_steps == self.number_steps:
            if self.state != "stalling":
                self.current_steps = 0  
            self.state = "stalling" 

    def animation(self):
        if self.moving:  # Only animate when moving
            animation = self.animations[self.direction]
            animation_speed = 0.2  # Control animation speed

            self.animation_counter += animation_speed
            if self.animation_counter >= len(animation):
                self.animation_counter = 0  # Loop animation

            index = int(self.animation_counter)  # Get current animation frame
            self.image = animation[index]
        else:
            self.animation_counter = 0  # Reset animation counter when not moving
            self.image = self.animations[self.direction][1]  # Keep first frame
        
    def collide_block(self, direction):
        for sprite in self.game.blocks:
            if self.rect.colliderect(sprite.rect):
                # On collision, set state to 'collision_reacting' and set direction
                self.state = "collision_reacting"
                self.handle_collision(sprite, direction)
                
    def handle_collision(self, sprite, direction):
        if direction == "horizontal":
            if self.x_change > 0:  # Moving right
                self.rect.right = sprite.rect.left  # Stop movement to the right
                self.direction = "left"  # Face left after collision
            elif self.x_change < 0:  # Moving left
                self.rect.left = sprite.rect.right  # Stop movement to the left
                self.direction = "right"  # Face right after collision

        if direction == "vertical":
            if self.y_change > 0:  # Moving down
                self.rect.bottom = sprite.rect.top  # Stop movement downward
                self.direction = "up"  # Face up after collision
            elif self.y_change < 0:  # Moving up
                self.rect.top = sprite.rect.bottom  # Stop movement upward
                self.direction = "down"  # Face down after collision
                                             
    def change_direction(self):
        # Get the list of all possible directions and remove the current one
        directions = ['left', 'right', 'up', 'down']
        directions.remove(self.direction)
        
        # Choose a random direction from the remaining ones
        self.direction = random.choice(directions)