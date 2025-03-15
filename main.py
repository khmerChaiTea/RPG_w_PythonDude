import pygame, sys
from settings import *
from sprites import *
from pygame.sprite import LayeredUpdates

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption('Basic RPG')
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Load spritesheets
        self.terrain_spritesheet = Spritesheet('assets/images/terrain.png')
        self.player_spritesheet = Spritesheet('assets/images/cats.png')
        self.enemy_spritesheet = Spritesheet('assets/images/evil.png')
        self.weapon_spritesheet = Spritesheet('assets/images/sword.png')
        self.bullet_spritesheet = Spritesheet('assets/images/powerBall.png')
        
        # Create sprite groups
        self.all_sprites = LayeredUpdates()
        self.blocks = pygame.sprite.Group()
        self.water = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()  # Single player
        self.weapons = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.healthbar = pygame.sprite.Group()
        
        self.create_tile_map()
        
    def create_tile_map(self):
        for i, row in enumerate(WORLD_MAP):
            for j, column in enumerate(row):
                ground = Ground(self, j, i)
                self.all_sprites.change_layer(ground, 1)
                
                if column == 'B':
                    block = Block(self, j, i)
                    self.blocks.add(block)  # Add block to blocks group
                    self.all_sprites.change_layer(block, 2)  # Set block layer
                if column == 'P':
                    self.player = Player(self, j, i)  # Player initialization
                    self.all_sprites.change_layer(self.player, 3)  # Set player layer
                    self.player_group.add(self.player)  # Add player to the player group
                if column == 'E':
                    enemy = Enemy(self, j, i)
                    self.enemies.add(enemy)  # Add enemy to enemies group
                    self.all_sprites.change_layer(enemy, 3)  # Set enemy layer

    def update(self, dt):
        self.player.update(dt)
        self.all_sprites.update(dt)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def draw(self):
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        pygame.display.update()
        self.clock.tick(FPS)
                    
    def main(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000  # Convert milliseconds to seconds
            self.handle_events()
            self.update(dt)
            self.draw()
        
if __name__ == "__main__":
    game = Game()
    game.main()
    pygame.quit()
    sys.exit()