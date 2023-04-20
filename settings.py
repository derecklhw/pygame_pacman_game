import pygame.mixer

pygame.init()

# screen settings
WIDTH, HEIGHT = 760, 670
TOP_BOTTOM_MARGIN = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH - TOP_BOTTOM_MARGIN - 150, HEIGHT - TOP_BOTTOM_MARGIN
FPS = 50
NUM_COLS = 28
NUM_ROWS = 30
HIGH_SCORE_AMOUNT = 5

# colour settings
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (169, 169, 169)
PALE_CANARY = (255, 255, 153)
PINK = (255, 102, 255)
ORANGE = (255, 102, 0)
ORANGE_YELLOW = (255, 204, 0)
LIGHT_ORANGE = (255, 148, 77)
LIGHT_BLUE = (153, 204, 255)
LIGHT_RED = (255, 102, 102)
LIGHT_GREY = (186, 186, 186)

# font settings
FONT = 'asset/emulogic.ttf'
START_FONT_SIZE = 20
PLAYING_FONT_SIZE = 16
GAME_OVER_FONT_SIZE = 40

# player settings
# PLAYER_START_POS = 0
PLAYER_COLOUR = (255, 255, 102)

# button settings
BUTTON_TEXT_SIZE = 20
BUTTON_TEXT_COLOUR = BLACK

# music settings
death_sound = pygame.mixer.Sound('asset/music/Death_Sound_pm.wav')
eat_sound = pygame.mixer.Sound('asset/music/Eat_Sound_1.wav')
pause_sound = pygame.mixer.Sound('asset/music/Pause_Sound.wav')
walking_ghost_sound = pygame.mixer.Sound('asset/music/Walking_Ghost.wav')