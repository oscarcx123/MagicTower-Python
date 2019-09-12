# 作为新框架测试用

import pygame
import os
import json
from sysconf import *

pygame.init()
# 设置游戏窗口大小
screen = pygame.display.set_mode([WIDTH, HEIGHT])
# 设置窗口标题
pygame.display.set_caption(TOWER_NAME)

from lib.utools import *
from lib import CurrentMap, PlayerCon
from lib.ground import GroundSurface
from lib import global_var
from project.function import function_init, draw_status_bar

RootScreen = GroundSurface(mode="copy", surface=screen)
global StatusBar
running = True
start_menu = True
from lib import ui
from lib import actions

action_control = actions.ActionControl()


def init():
    # 初始化全局变量
    global_var._init()
    global_var.set_value("font_name", FONT_NAME)
    global_var.set_value("RootScreen", RootScreen)
    global_var.set_value("action_control", action_control)

    # 延迟map初始化，避免文件的循环引用
    CurrentMap.lib_map_init()
    # 设置PlayerCon为全局变量（必须要在CurrentMap.set_map之前完成）
    global_var.set_value("PlayerCon", PlayerCon)
    function_init()
    
    # 初始化地图
    CurrentMap.set_map(PLAYER_FLOOR)
    CurrentMap.add_sprite(PlayerCon)
    global_var.set_value("CurrentMap", CurrentMap)
    # 状态栏
    StatusBar = RootScreen.add_child("left", BLOCK_UNIT * 4)
    global_var.set_value("StatusBar", StatusBar)
    RootScreen.add_child(CurrentMap)
    # 绘制状态栏
    draw_status_bar()
    # 初始化UI图层
    # --- UI1 - 怪物手册
    BOOK = ui.Book(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    BOOK.priority = 5  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(BOOK)
    global_var.set_value("BOOK", BOOK)
    # --- UI2 - 开始界面
    STARTMENU = ui.StartMenu(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    STARTMENU.priority = 10  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(STARTMENU)
    global_var.set_value("STARTMENU", STARTMENU)
    # --- UI3 - 背包界面
    BACKPACK = ui.Backpack(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    BACKPACK.priority = 5  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(BACKPACK)
    global_var.set_value("BACKPACK", BACKPACK)
    # --- UI4 - 存档界面
    SAVE = ui.SaveMenu(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    SAVE.priority = 5  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(SAVE)
    global_var.set_value("SAVE", SAVE)
    # --- UI5 - 读档界面
    LOAD = ui.LoadMenu(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    LOAD.priority = 5  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(LOAD)
    global_var.set_value("LOAD", LOAD)


def init_actions():
    # QUIT:
    def quit(e):
        global running
        running = False
        return True
    # 注册事件
    action_control.register_action('QUIT', pygame.QUIT, quit)
    action_control.register_action('BOOK', pygame.KEYUP, global_var.get_value('BOOK').action)
    action_control.register_action('STARTMENU', pygame.KEYUP, global_var.get_value('STARTMENU').action)
    action_control.register_action('BACKPACK', pygame.KEYUP, global_var.get_value('BACKPACK').action)
    action_control.register_action('SAVE', pygame.KEYUP, global_var.get_value('SAVE').action)
    action_control.register_action('LOAD', pygame.KEYUP, global_var.get_value('LOAD').action)
    print("事件全部注册完成！")

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
init_actions()
clock = pygame.time.Clock()

# 主程序
while running:
    # 展示开始菜单
    if start_menu == True:
        start = global_var.get_value("STARTMENU")
        start.open()
        start_menu = False

    pygame.display.update()
    # clock.tick(60)

    # 背景
    # RootScreen.fill_surface(load_image("img/ground.png"), mode="repeat")
    RootScreen.fill(GREEN)
    RootScreen.flush(screen)  # 显示刷新到屏幕
    action_control.action_render()  # 检查动作消息
