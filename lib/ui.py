# ui.py负责绘制各种文字（未来包括图片？）

import pygame
from sysconf import *
import lib

def init_ui():
    from test import StatusBar
    global StatusBar
    init_font()

def init_font():
    global font_name
    font_name = pygame.font.match_font(FONT_NAME)

# draw_text 接受GroundSurface（画板），text（需要显示的文字），size（文字大小），color（文字颜色），x，y（xy相对坐标）
def draw_text(GroundSurface, text, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    text_GroundSurface = font.render(text, True, color)
    text_rect = text_GroundSurface.get_rect()
    text_rect.left = x * BLOCK_UNIT
    text_rect.top = y * BLOCK_UNIT
    GroundSurface.surface.blit(text_GroundSurface, text_rect)

# TODO: 状态栏可能实现局部刷新？这里预留初了始化以及刷新状态栏的函数名
def init_status_bar():
    draw_status_bar()

def update_status_bar():
    StatusBar.fill(BLUE)
    draw_status_bar()


def draw_status_bar():
    draw_text(StatusBar, "FLOOR = " + str(lib.PlayerCon.floor), 36, WHITE, 0, 0)
    draw_text(StatusBar, "HP = " + str(lib.PlayerCon.hp), 36, WHITE, 0, 1)
    draw_text(StatusBar, "ATK = " + str(lib.PlayerCon.attack), 36, WHITE, 0, 2)
    draw_text(StatusBar, "DEF = " + str(lib.PlayerCon.defend), 36, WHITE, 0, 3)
    draw_text(StatusBar, "MDEF = " + str(lib.PlayerCon.mdefend), 36, WHITE, 0, 4)
    draw_text(StatusBar, "GOLD = " + str(lib.PlayerCon.gold), 36, WHITE, 0, 5)
    draw_text(StatusBar, "EXP = " + str(lib.PlayerCon.exp), 36, WHITE, 0, 6)
    draw_text(StatusBar, "Y_KEY = " + str(lib.PlayerCon.yellowkey), 36, WHITE, 0, 7)
    draw_text(StatusBar, "B_KEY = " + str(lib.PlayerCon.bluekey), 36, WHITE, 0, 8)
    draw_text(StatusBar, "R_KEY = " + str(lib.PlayerCon.redkey), 36, WHITE, 0, 9)