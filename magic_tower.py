# Python Magic Tower by Azure (oscarcx123)
import pygame
import random
import math
from os import path
from tower_database import get_monster_data
from tower_database import MAP_DATABASE

# --- Hero Data Setting START ---
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

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magic Tower")
clock = pygame.time.Clock()
font_name = pygame.font.match_font("arial")


# --- Functions START ---
# Drawing / Rendering functions
# draw_text receives drawing surface, text, size of text, text coordinates (upper left corner)
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.left = x * BLOCK_UNIT
    text_rect.top = y * BLOCK_UNIT
    surface.blit(text_surface, text_rect)


# draw_background is used to draw the ground tiles
def draw_background():
    # Start from "4 * BLOCK_UNIT" because the left hand side is the hero's status bar
    start_x = 4 * BLOCK_UNIT
    start_y = 0
    temp_x = start_x
    temp_y = start_y
    while temp_y < HEIGHT:
        while temp_x < WIDTH:
            screen.blit(background, (temp_x, temp_y))
            temp_x += BLOCK_UNIT
        temp_y += BLOCK_UNIT
        temp_x = start_x


# draw_map is used to paint everything on map besides the ground tiles
def draw_map(map_data):
    start_x = 0
    start_y = 0
    temp_x = start_x
    temp_y = start_y
    while temp_y < HEIGHT / BLOCK_UNIT:
        while temp_x < WIDTH / BLOCK_UNIT - 4:
            map_element = map_data[temp_y][temp_x]
            if int(map_element) != 0:
                name = "img_" + str(map_element)
                screen.blit(eval(name), ((temp_x + 4) * BLOCK_UNIT, temp_y * BLOCK_UNIT))
            temp_x += 1
        temp_y += 1
        temp_x = start_x


# draw_status_bar is used to draw the text on the status bar
def draw_status_bar():
    draw_text(screen, "FLOOR = " + str(player.floor), 36, 0, 0)
    draw_text(screen, "HP = " + str(player.hp), 36, 0, 1)
    draw_text(screen, "ATK = " + str(player.attack), 36, 0, 2)
    draw_text(screen, "DEF = " + str(player.defend), 36, 0, 3)
    draw_text(screen, "MDEF = " + str(player.mdefend), 36, 0, 4)
    draw_text(screen, "GOLD = " + str(player.gold), 36, 0, 5)
    draw_text(screen, "EXP = " + str(player.exp), 36, 0, 6)
    draw_text(screen, "Y_KEY = " + str(player.yellowkey), 36, 0, 7)
    draw_text(screen, "B_KEY = " + str(player.bluekey), 36, 0, 8)
    draw_text(screen, "R_KEY = " + str(player.redkey), 36, 0, 9)


# crop_images is used to split the image (64, 64) from the resources (32x, 32)
def crop_images(image, prefix, start_num, height, width):
    for i in range(int(height * 2 / BLOCK_UNIT)):
        empty_surf = pygame.Surface((width, int(BLOCK_UNIT * i)))
        empty_surf.blit(image, (0, -BLOCK_UNIT * (i - 1)))
        empty_surf = pygame.transform.chop(empty_surf, (0, width, 0, BLOCK_UNIT * (i - 1)))
        empty_surf.set_colorkey(BLACK)
        name = prefix + str(i + start_num)
        globals()[name] = empty_surf


# Rules functions
# can_pass is used to determine whether a destination is passable or not. It returns a boolean value.
def can_pass(direction):
    if direction == "left":
        if (player.rect.left / BLOCK_UNIT) - 4 > 0:  # Check whether the player is located next to the boarder
            map_data = map_read(player.floor)
            row = int(player.rect.top / BLOCK_UNIT)
            column = int(player.rect.left / BLOCK_UNIT) - 5
            map_object = map_data[row][column]  # read from the map_data to see what's at the destination
            if detect_events(map_object, row, column):
                return True
            else:
                return False

    if direction == "right":
        if (player.rect.left / BLOCK_UNIT) - 4 < 12:
            map_data = map_read(player.floor)
            row = int(player.rect.top / BLOCK_UNIT)
            column = int(player.rect.left / BLOCK_UNIT) - 3
            map_object = map_data[row][column]
            if detect_events(map_object, row, column):
                return True
            else:
                return False

    if direction == "up":
        if player.rect.top / BLOCK_UNIT > 0:
            map_data = map_read(player.floor)
            row = int(player.rect.top / BLOCK_UNIT) - 1
            column = int(player.rect.left / BLOCK_UNIT) - 4
            map_object = map_data[row][column]
            if detect_events(map_object, row, column):
                return True
            else:
                return False

    if direction == "down":
        if (player.rect.top / BLOCK_UNIT) < 12:
            map_data = map_read(player.floor)
            row = int(player.rect.top / BLOCK_UNIT) + 1
            column = int(player.rect.left / BLOCK_UNIT) - 4
            map_object = map_data[row][column]
            if detect_events(map_object, row, column):
                return True
            else:
                return False


# Tool functions
# get_damage_info is used to "simulate" a battle so it's a crutial function
# It can be used by the monster manual or a real battle
def get_damage_info(map_object):
    # Get monster stats
    # get_monster_data is located in "tower_database.py"
    monster_stats = get_monster_data(map_object)
    mon_name = monster_stats["name"]
    mon_hp = monster_stats["hp"]
    mon_atk = monster_stats["atk"]
    mon_def = monster_stats["def"]
    mon_gold = monster_stats["money"]
    mon_exp = monster_stats["experience"]
    # Check if hero_atk > mon_def
    if player.attack < mon_def:
        return False
    # Calculate damage taken by player per turn
    damage_from_mon_per_turn = mon_atk - player.defend
    # Damage taken by player can't be negative
    if damage_from_mon_per_turn < 0:
        damage_from_mon_per_turn = 0
    # Calculate damage taken by monster per turn
    damage_from_hero_per_turn = player.attack - mon_def
    # Calculate the amount of turns to kill the monster
    turn = math.ceil(mon_hp / damage_from_hero_per_turn)
    # Calculate damage
    damage = damage_from_mon_per_turn * (turn - 1) - player.mdefend
    # Negative damage (Heal up the hero) is now allowed
    if damage < 0:
        damage = 0
    result = {"damage": damage, "mon_gold": mon_gold, "mon_exp": mon_exp}
    return result


# Check if something is on the map
def check_map(floor, target):
    map_temp = map_database[floor - 1]
    start_x = 0
    start_y = 0
    temp_x = start_x
    temp_y = start_y
    while temp_y < HEIGHT / BLOCK_UNIT:
        while temp_x < WIDTH / BLOCK_UNIT - 4:
            if map_temp[temp_y][temp_x] == target:
                return {"result": True, "y_coordinate": temp_y, "x_coordinate": temp_x}
            temp_x += 1
        temp_y += 1
        temp_x = 0
    return {"result": False}


# Events functions
# detect_events determine the event function that should be triggered
def detect_events(map_object, row, column):
    # According to HTML5 Magic Tower,
    # 0 = Nothing (No obstacle)
    # 1 = Wall (blocks the player)
    # 21 - 69 = Items (Player can step on it and get the item)
    # 81 - 86 = Doors (player can't step on but instead open it)
    # 201+ = Monsters (trigger battle)
    if map_object == 0:
        return True
    else:
        if map_object == 1:
            return False
        elif map_object >= 21 and map_object <= 69:
            get_item(map_object, row, column)
            return True
        # Skip special door here because it should be triggered by something other events
        elif map_object >= 81 and map_object <= 84 or map_object == 86:
            open_door(map_object, row, column)
            return False
        elif map_object >= 87 and map_object <= 88:
            if map_object == 87:
                change_floor("go_upstairs", row, column)
            elif map_object == 88:
                change_floor("go_downstairs", row, column)
            return False
        elif map_object >= 201:
            battle(map_object, row, column)
            return False
        else:
            return False


# battle is used to determine the aftermath of a battle
def battle(map_object, row, column):
    result = get_damage_info(map_object)
    # Check if the monster is unbeatable
    if result == False:
        return False
    # Check if the player will be killed
    else:
        if result["damage"] >= player.hp:
            # Will not initiate the battle if player is going to be killed
            return False
        else:
            # Calculate the stats of player after battle
            player.hp -= result["damage"]
            player.gold += result["mon_gold"]
            player.exp += result["mon_exp"]
            map_write(player.floor, row, column, 0)
            return True


def get_item(map_object, row, column):
    print("item test success")


# open_door can open the door if requirements are met
def open_door(map_object, row, column):
    if map_object == 81 and player.yellowkey > 0:
        player.yellowkey -= 1
        map_write(player.floor, row, column, 0)
    elif map_object == 82 and player.bluekey > 0:
        player.bluekey -= 1
        map_write(player.floor, row, column, 0)
    elif map_object == 83 and player.redkey > 0:
        player.redkey -= 1
        map_write(player.floor, row, column, 0)
    elif map_object == 84 and player.greenkey > 0:
        player.greenkey -= 1
        map_write(player.floor, row, column, 0)
    elif map_object == 85:
        map_write(player.floor, row, column, 0)
    elif map_object == 86:
        if STEEL_DOOR_NEEDS_KEY:
            if player.steelkey > 0:
                player.steelkey -= 1
                map_write(player.floor, row, column, 0)
        else:
            map_write(player.floor, row, column, 0)


# Change floor can change the floor and it can be used without a stair
# change_floor(destination floor, y, x)
def change_floor(floor, row, column):
    if floor == "go_upstairs":
        check_map_result = check_map(player.floor + 1, 88)
        if check_map_result["result"] == True:
            x_coordinate = check_map_result["x_coordinate"]
            y_coordinate = check_map_result["y_coordinate"]
            player.rect.top = y_coordinate * BLOCK_UNIT
            player.rect.left = (x_coordinate + 4) * BLOCK_UNIT
        player.floor += 1
    elif floor == "go_downstairs":
        check_map_result = check_map(player.floor - 1, 87)
        if check_map_result["result"] == True:
            x_coordinate = check_map_result["x_coordinate"]
            y_coordinate = check_map_result["y_coordinate"]
            player.rect.top = y_coordinate * BLOCK_UNIT
            player.rect.left = (x_coordinate + 4) * BLOCK_UNIT
        player.floor -= 1
    # When this function is not triggered by stairs
    else:
        x_coordinate = column
        y_coordinate = row
        player.rect.top = y_coordinate * BLOCK_UNIT
        player.rect.left = (x_coordinate + 4) * BLOCK_UNIT
        player.floor = floor


# Data Functions
# map_read can read data from map_database
def map_read(floor):
    map_index = floor - 1
    map_data = map_database[map_index]
    return map_data


# map_write can write data to map_database
def map_write(floor, row, column, change):
    map_index = floor - 1
    map_database[map_index][row][column] = change


# --- Functions END ---

# --- Class START ---

# *** 修改为继承自ActorSprite类（权宜之计用来测试 后面还是分离开）
from sprite import ActorSprite


class Player(ActorSprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (64 * 4, 64 * 4))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.top = Y_COORDINATE * BLOCK_UNIT
        self.rect.left = (X_COORDINATE + 4) * BLOCK_UNIT

        ActorSprite.__init__(self, 0, self.image, [X_COORDINATE + 4, Y_COORDINATE], [4, 4])

        self.speedx = 0
        self.speedy = 0
        self.hp = PLAYER_HP
        self.attack = PLAYER_ATK
        self.defend = PLAYER_DEF
        self.mdefend = PLAYER_MDEF
        self.gold = PLAYER_GOLD
        self.exp = PLAYER_EXP
        self.yellowkey = PLAYER_YELLOWKEY
        self.bluekey = PLAYER_BLUEKEY
        self.redkey = PLAYER_REDKEY
        self.greenkey = PLAYER_GREENKEY
        self.steelkey = PLAYER_STEELKEY
        self.floor = PLAYER_FLOOR

    def update(self):
        print(self.pos)
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            if can_pass("left"):
                self.speedx = -BLOCK_UNIT
                # ***
                self.move(1)
        elif keystate[pygame.K_RIGHT]:
            if can_pass("right"):
                # ***
                self.move(2)
                self.speedx = BLOCK_UNIT
        elif keystate[pygame.K_UP]:
            if can_pass("up"):
                # ***
                self.move(3)
                self.speedy = -BLOCK_UNIT
        elif keystate[pygame.K_DOWN]:
            if can_pass("down"):
                # ***
                self.move(0)
                self.speedy = BLOCK_UNIT
        ActorSprite.update(self)
        return

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 4 * BLOCK_UNIT:
            self.rect.left = 4 * BLOCK_UNIT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


# --- Class END ---

# --- Loading Resources START ---
# Load map data
map_database = MAP_DATABASE  # MAP_DATABASE is located in "tower_database.py"

# Load ALL game graphics
# Load background tiles
background_original = pygame.image.load(path.join(img_dir, "ground.png")).convert()
background = pygame.transform.scale(background_original, (64, 64))
background_rect = background.get_rect()
# Load Player image
player_img = pygame.image.load(path.join(img_dir, "hero48.png")).convert()
# Load wall image
wall_original = pygame.image.load(path.join(img_dir, "wall.png")).convert()
img_1 = pygame.transform.scale(wall_original, (64, 64))
# Load enemy images
enemies_full_black_original = pygame.image.load(path.join(img_dir, "enemies_full_black.png")).convert()
enemies_full_black_original_rect = enemies_full_black_original.get_rect()
width = enemies_full_black_original_rect.right
height = enemies_full_black_original_rect.bottom
enemies_full_black_img = pygame.transform.scale(enemies_full_black_original, (width * 2, height * 2))
enemies_full_black_img.set_colorkey(BLACK)
surf_mon_full = pygame.Surface((width, height * 2))
surf_mon_full.blit(enemies_full_black_img, (0, 0))
crop_images(surf_mon_full, "img_", 200, height, width)
# Load Jewel images
jewels = pygame.image.load(path.join(img_dir, "jewels.png")).convert()
jewels_rect = jewels.get_rect()
width = jewels_rect.right
height = jewels_rect.bottom
jewels_img = pygame.transform.scale(jewels, (width * 2, height * 2))
jewels_img.set_colorkey(BLACK)
crop_images(jewels_img, "img_", 26, height * 2, width * 2)
# Load potion images
potions = pygame.image.load(path.join(img_dir, "potions.png")).convert()
potions_rect = potions.get_rect()
width = potions_rect.right
height = potions_rect.bottom
potions_img = pygame.transform.scale(potions, (width * 2, height * 2))
potions_img.set_colorkey(BLACK)
crop_images(potions_img, "img_", 30, height * 2, width * 2)
# Load key images
keys = pygame.image.load(path.join(img_dir, "keys.png")).convert()
keys_rect = keys.get_rect()
width = keys_rect.right
height = keys_rect.bottom
keys_img = pygame.transform.scale(keys, (width * 2, height * 2))
keys_img.set_colorkey(BLACK)
crop_images(keys_img, "img_", 20, height * 2, width * 2)
# Load door images
doors = pygame.image.load(path.join(img_dir, "doors.png")).convert()
doors_rect = doors.get_rect()
width = doors_rect.right
height = doors_rect.bottom
doors_img = pygame.transform.scale(doors, (width * 2, height * 2))
doors_img.set_colorkey(BLACK)
crop_images(doors_img, "img_", 80, height * 2, width * 2)
# Load stair images
stairs = pygame.image.load(path.join(img_dir, "stairs.png")).convert()
stairs_rect = stairs.get_rect()
width = stairs_rect.right
height = stairs_rect.bottom
stairs_img = pygame.transform.scale(stairs, (width * 2, height * 2))
stairs_img.set_colorkey(BLACK)
crop_images(stairs_img, "img_", 86, height * 2, width * 2)

# Load all game sounds
pygame.mixer.music.load(path.join(snd_dir, "AxiumCrisis.ogg"))
pygame.mixer.music.set_volume(0.3)
# some_sound = pygame.mixer.Sound(path.join(snd_dir, "some.wav"))
pygame.mixer.music.play(loops=-1)  # Keeps the background music on loop

# Load Sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
# --- Loading Resources END ---

# --- Game START---
running = True
while running:
    # Keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Updates
    all_sprites.update()

    # Draw / Render Graphics
    screen.fill(BLUE)
    draw_background()  # Draw the tiles
    draw_map(map_read(player.floor))
    draw_status_bar()  # Hero status on the left side
    all_sprites.draw(screen)
    # After drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
# --- Game END---
