from os import path

# 系统设置 其他地方都会用到这里的配置

# 全塔属性设置
TOWER_NAME = "Python魔塔"
FONT_NAME = "resource/simhei.ttf"
DEBUG = False
# SAVE_MAX_AMOUNT为最大允许存档数量
SAVE_MAX_AMOUNT = 100
# 玩家移动速度（移动一格所需要的毫秒数 & 换腿所需时间的两倍）
PLAYER_SPEED = 125
# --- 勇士数据设置 START ---
# 玩家初始坐标以及楼层
# face[0]调用勇士朝向 0=下，1=左，2=右，3=上
X_COORDINATE = 6
Y_COORDINATE = 10
PLAYER_FLOOR = 0
# 玩家初始属性
PLAYER_HP = 815
PLAYER_ATK = 10
PLAYER_DEF = 8
PLAYER_MDEF = 0
PLAYER_GOLD = 0
PLAYER_EXP = 0
PLAYER_ITEM = {21:2,23:2,24:10,47:10,57:2,26:1,49:3,50:3,51:2,52:2,56:5,68:5,69:3}
# --- 勇士数据设置 END ---

# 怪物特殊属性参数

MON_ABILITY_VALUE = {
    "poisonDamage": 10,
    "weakValue": 20,
    "breakArmor": 0.9,
    "counterAttack": 0.1,
    "purify": 3,
    "hatred": 2,
}


# --- 物品/道具数据设置 START ---
# 宝石
RED_JEWEL = 2
BLUE_JEWEL = 2
GREEN_JEWEL = 4
YELLOW_JEWEL = 1
# 血瓶
RED_POTION = 100
BLUE_POTION = 200
GREEN_POTION = 400
YELLOW_POTION = 800
# 装备
SWORD_1 = 7
SHIELD_1 = 7
SWORD_2 = 20
SHIELD_2 = 20
SWORD_3 = 14
SHIELD_3 = 14
SWORD_4 = 80
SHIELD_4 = 80
SWORD_5 = 160
SHIELD_5 = 160

# 【可选】设置
STEEL_DOOR_NEEDS_KEY = True
BIG_KEY_OPEN_YELLOW_DOORS = True
# --- 道具数据设置 END ---


# --- 基本常数 START ---
# 定义游戏属性
SIDE_BLOCK_COUNT = 13
WIDTH = (13 + 4) * 64  # 1088  # (13 + 4) * 64
HEIGHT = 13 * 64  # 832  # 13 * 64
# BLOCK_UNIT 定义每格大小
BLOCK_UNIT = HEIGHT / 13  # BLOCK_UNIT = 64
FPS = 120  # 每秒帧数
MSPF = int(1000 / FPS)  # 每一帧毫秒数
DEFAULT_SPEED = 500  # 默认动画速度(周期)

RESOURCE_SCALE = BLOCK_UNIT / 32

true = True
false = False
null = None

# 定义图片，音乐的路径
img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "sound")
bgm_dir = path.join(snd_dir, "BGM")
se_dir = path.join(snd_dir, "SE")

## 定义颜色
# 红色系
RED = (255, 0, 0)
DARKRED = (139, 0, 0)
# 橙色系
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
DARKORANGE = (255, 140, 0)
# 黄色系
LIGHTYELLOW = (255, 255, 224)
YELLOW = (255, 255, 0)
# 绿色系
LIME = (0, 255, 0)
LIMEGREEN = (50, 205, 50)
GREEN = (0, 128, 0)
SPRINGGREEN = (0, 255, 127)
SEAGREEN = (46, 139, 87)
OLIVE = (128, 128, 0)
# 青色系
CYAN = (0, 255, 255)
DARKCYAN = (0, 139, 139)
# 蓝色系
LIGHTSKYBLUE = (135, 206, 250)
SKYBLUE = (135, 206, 235)
DEEPSKYBLUE = (0, 191, 255)
LIGHTSTEELBLUE = (176, 196, 222)
BLUE = (0, 0, 255)
MEDIUMBLUE = (0, 0, 205)
DARKBLUE = (0, 0, 139)
# 紫色系
VIOLET = (238, 130, 238)
FUCHSIA = (255, 0, 255)
PURPLE = (128, 0, 128)
INDIGO = (75, 0, 130)
# 粉色系
PINK = (255, 192, 203)
LIGHTPINK = (255, 182, 193)
DEEPPINK = (255, 20, 147)
# 白色系
WHITE = (255, 255, 255)
SNOW = (255, 250, 250)
AZURE = (240, 255, 255)
# 灰色系
LIGHTGRAY = (211, 211, 211)
SILVER = (192, 192, 192)
DARKGRAY = (169, 169, 169)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
# 棕色系
WHEAT = (245, 222, 179)
CHOCOLATE = (210, 105, 30)
BROWN = (165, 42, 42)
# --- 基本常数 END ---
