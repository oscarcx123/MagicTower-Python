# 作为新框架测试用

import pygame
from sysconf import *

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

from lib.utools import *
from project.floors import MAP_DATABASE
from lib import CurrentMap, PlayerCon
from lib.ground import GroundSurface
from lib import global_var
from project.function import function_init, draw_status_bar

RootScreen = GroundSurface(screen)
global StatusBar


def init():
    # 初始化全局变量
    global_var._init()
    global_var.set_value("font_name",pygame.font.match_font(FONT_NAME))
    # 延迟map初始化，避免文件的循环引用
    CurrentMap.lib_map_init()
    # 设置PlayerCon为全局变量（必须要在CurrentMap.set_map之前完成）
    global_var.set_value("PlayerCon", PlayerCon)
    function_init()
    # 初始化地图
    CurrentMap.set_map(MAP_DATABASE[PLAYER_FLOOR])
    CurrentMap.add_sprite(PlayerCon)
    # 状态栏
    StatusBar = RootScreen.add_child("left", BLOCK_UNIT*4)
    global_var.set_value("StatusBar",StatusBar)
    RootScreen.add_child(CurrentMap)
    # 绘制状态栏
    draw_status_bar()

# ===== debug === 发布模式注释下面内容
import threading

running = True


def console():
    while running:
        r = input()
        try:
            print(eval(r))
        except:
            try:
                exec(r)
            except Exception as e:
                print("error:", str(e))


t = threading.Thread(target=console)

t.start()

# ===============================#

init()
clock = pygame.time.Clock()

while running:
    pygame.display.update()
    # clock.tick(60)

    # 背景
    # RootScreen.fill_surface(load_image("img/ground.png"), mode="repeat")
    RootScreen.fill(GREEN)
    RootScreen.flush()  # 显示刷新

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
