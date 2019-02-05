# 作为新框架测试用

import pygame
from sysconf import *

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

from lib.utools import *

from project.floors import MAP_DATABASE
from lib import CurrentMap, PlayerCon

from lib.ground import GroundSurface
RootScreen = GroundSurface(screen)
StatusBar = None

def init():
    global StatusBar
    CurrentMap.set_map(MAP_DATABASE[PLAYER_FLOOR - 1])
    CurrentMap.add_sprite(PlayerCon)
    StatusBar = RootScreen.add_child("left", 256)  # 状态栏
    RootScreen.add_child(CurrentMap)
    StatusBar.fill(BLUE)
    # 可对状态栏进行操作


# ===== debug ===
import threading


def console():
    while True:
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
running = True
while running:
    pygame.display.update()

    # 背景
    # RootScreen.fill_surface(load_image("img/ground.png"), mode="repeat")
    RootScreen.fill(GREEN)
    RootScreen.flush()  # 显示刷新

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
