import pygame, sys
from settings import *
from sprites import *
from groups import AllSprites

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Basic RPG')
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create sprite groups
        self.all_sprites = AllSprites()
        self.blocks = pygame.sprite.Group()
        self.water = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()  # Single player
        self.weapons = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.healthbar = pygame.sprite.Group()
        
        self.create_tile_map()
        
    def create_tile_map(self):
        pass
    
    def update(self):
        self.all_sprites.update()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.update()
        self.clock.tick(FPS)
                    
    def main(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
        
if __name__ == "__main__":
    game = Game()
    game.main()
    pygame.quit()
    sys.exit()