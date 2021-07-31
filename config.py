# Configurations for the entire game:

# Grid Configurations
FRAME_RATE = 10000

GRID_CONFIG = {'HEIGHT': 30, 'WIDTH': 80, 'CODE': {
    'BLANK': 0, 'PLAYER': 1, 'ENEMY': 2, 'OBSTACLE': 3, 'CLOUD': 4, 'EXIT': 5,
    'GRASS': 6, 'COIN': 7}, 'ACTUAL_WIDTH': 400, 'ACTUAL_HEIGHT': 32}
PLAYER_CONFIG = {'SIZE': 3, 'START_LIVES': 5, 'LIVES_LOST': 0}
ENEMY_CONFIG = {'SIZE': 2, 'DIRECTIONS': ['LEFT', 'RIGHT']}

LEVEL = 1
NUM_LEVELS = 3
