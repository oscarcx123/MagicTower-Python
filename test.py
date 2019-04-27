# 作为新框架测试用

import pygame
from sysconf import *

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

from lib.utools import *
from project.floors import MAP_DATABASE
from lib import CurrentMap, PlayerCon
from lib.ground import GroundSurface
from lib import ui

RootScreen = GroundSurface(screen)
StatusBar = None


def init():
    global StatusBar
    CurrentMap.set_map(MAP_DATABASE[PLAYER_FLOOR])
    CurrentMap.add_sprite(PlayerCon)
    StatusBar = RootScreen.add_child("left", BLOCK_UNIT*4)  # 状态栏
    RootScreen.add_child(CurrentMap)
    StatusBar.fill(BLUE)
    # 可对状态栏进行操作
    ui.init_ui()
    ui.init_status_bar()


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

init()
clock = pygame.time.Clock()

# ===============================#

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