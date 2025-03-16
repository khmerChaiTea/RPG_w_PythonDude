# Window size
WIN_WIDTH = 800
WIN_HEIGHT = 600

# Tile size
TILESIZE = 32

# Frames per second (FPS)
FPS = 60

# Layer definitions
HEALTH_LAYER = 6
PLAYER_LAYER = 5
WEAPON_LAYER = 7
ENEMY_LAYER = 3
BLOCKS_LAYER = 2
GROUND_LAYER = 1

# Movement steps
PLAYER_STEPS = 85 # Adjust speed as needed (200 pixels per second when use with dt)
ENEMY_STEPS = 80
BULLET_STEPS = 6

# Health values
ENEMY_HEALTH = 6
PLAYER_HEALTH = 10

# Colors (RGB tuples)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BG_COLOR = (50, 50, 50)

# Tilemap layout
WORLD_MAP = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B........BBB.............................................B',
    'B.........B..............................................B',
    'B.E.......B...E..........................................B',
    'B.....................................................B..B',
    'B............................................BBB.........B',
    'B........B.RR.........................................BB.B',
    'B........B.......................................RR....E.B',
    'B..BB.....P.W............................................B',
    'BE............E..........................................B',
    'B...........................................BBBBB......RRB',
    'B..E...................................................RRB',
    'BE......................................................RB',
    'B........................................................B',
    'B........................................................B',
    'B........................................................B',
    'B..........................R.............................B',
    'B..........................R......................... ...B',
    'B..........................R.............................B',
    'B..........................R.............................B',
    'B........RRRRRRRRRRRRRRRRRRR.............................B',
    'B........RRRRRRRRRRRRRRRRRRR.............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]