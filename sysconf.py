# 系统设置 其他地方都会用到这里的配置


# --- Hero Data Setting START ---
from os import path
# Initial Coordinate for Hero (Player)
X_COORDINATE = 6
Y_COORDINATE = 10
PLAYER_FLOOR = 1
# Initial Stats for Hero (Player)
PLAYER_HP = 1000
PLAYER_ATK = 10
PLAYER_DEF = 5
PLAYER_MDEF = 10
PLAYER_GOLD = 100
PLAYER_EXP = 0
PLAYER_YELLOWKEY = 3
PLAYER_BLUEKEY = 2
PLAYER_REDKEY = 1
PLAYER_GREENKEY = 1
PLAYER_STEELKEY = 1
# --- Hero Data Setting END ---

# --- Optional Setting START ---
STEEL_DOOR_NEEDS_KEY = True
# --- Optional Setting END ---

# --- Basic Constants START ---
# Define some properties of the game
WIDTH = 1088  # (13 + 4) * 64
HEIGHT = 832  # 13 * 64
# BLOCK_UNIT is used to create "invisible tiles" later. In this case the size of a block is 64 * 64 instead of 32 * 32
BLOCK_UNIT = HEIGHT / 13  # BLOCK_UNIT = 64
FPS = 12

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define directories for images and sounds
img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "sound")
# --- Basic Constants END ---
