# 作为新框架测试用

import pygame
from sysconf import *

pygame.init()
# 设置游戏窗口大小
screen = pygame.display.set_mode([WIDTH, HEIGHT])
# 设置窗口标题
pygame.display.set_caption(TOWER_NAME)

from lib.utools import *
from project.floors import MAP_DATABASE
from lib import CurrentMap, PlayerCon
from lib.ground import GroundSurface
from lib import global_var
from project.function import function_init, draw_status_bar, draw_start_menu, wait_start_menu, draw_enemy_book, wait_enemy_book

RootScreen = GroundSurface(screen)
global StatusBar
running = True
start_menu = True

def init(): 
    # 初始化全局变量
    global_var._init()
    global_var.set_value("font_name",FONT_NAME)
    global_var.set_value("RootScreen",RootScreen)
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

# DEBUG（开关在sysconf.py，如果开启将会启动控制台）
if DEBUG:
    import threading
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

# 主程序
while running:
    # 展示开始菜单
    if start_menu == True:
        draw_start_menu()
        wait_start_menu()
        start_menu = False
    
    pygame.display.update()
    # clock.tick(60)

    # 背景
    # RootScreen.fill_surface(load_image("img/ground.png"), mode="repeat")
    RootScreen.fill(GREEN)
    RootScreen.flush() # 显示刷新

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_x:
                draw_enemy_book()
                wait_enemy_book()
