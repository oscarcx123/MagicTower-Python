import math
import pygame
from lib import CurrentMap
from project.enemy import *
from project.block import BlockData
from project.items import ITEMS_DATA
from project.floors import MAP_DATABASE
from lib import global_var


# function_init 初始化（从全局变量获取PlayerCon）
def function_init():
    global PlayerCon
    PlayerCon = global_var.get_value("PlayerCon")
    global RootScreen
    RootScreen = global_var.get_value("RootScreen")

# flush_status 刷新地图&状态栏显示
def flush_status():
    # 刷新地图显示
    CurrentMap.draw_map()
    # 刷新状态栏显示
    draw_status_bar()

# get_damage_info 获取战斗伤害（模拟战斗）
def get_damage_info(map_object):
    # 通过get_enemy_info获得怪物数据
    monster_stats = get_enemy_info(map_object)
    mon_name = monster_stats["name"]
    mon_hp = monster_stats["hp"]
    mon_atk = monster_stats["atk"]
    mon_def = monster_stats["def"]
    mon_gold = monster_stats["money"]
    mon_exp = monster_stats["experience"]
    # 检测勇士能否破怪物防御
    if PlayerCon.attack <= mon_def:
        return {"status": False,
                "mon_name": mon_name,
                "mon_hp": mon_hp,
                "mon_atk": mon_atk,
                "mon_def": mon_def,
                "mon_gold": mon_gold,
                "mon_exp": mon_exp,
                "damage": "???"}
    # 计算每回合勇士受到的伤害
    damage_from_mon_per_turn = mon_atk - PlayerCon.defend
    # 勇士受到伤害是否 < 0
    if damage_from_mon_per_turn < 0:
        damage_from_mon_per_turn = 0
    # 计算每回合勇士对怪物造成的伤害
    damage_from_hero_per_turn = PlayerCon.attack - mon_def
    # 计算勇士击杀怪物所需的回合数
    turn = math.ceil(mon_hp / damage_from_hero_per_turn)
    # 计算勇士本次战斗所受到的伤害
    damage = damage_from_mon_per_turn * (turn - 1) - PlayerCon.mdefend
    # 勇士不允许受到负数伤害（治疗）
    if damage < 0:
        damage = 0
    result = {"status": True,
                "mon_name": mon_name,
                "mon_hp": mon_hp,
                "mon_atk": mon_atk,
                "mon_def": mon_def,
                "mon_gold": mon_gold,
                "mon_exp": mon_exp,
                "damage": damage}
    return result

# get_enemy_info 获得怪物数据
def get_enemy_info(map_object):
    # 从/project/block.py获取怪物id
    monster_id = BlockData[str(map_object)]["id"]
    # 从/project/enemy.py获取怪物详细数据
    monster_stats = MONSTER_DATA[monster_id]
    return monster_stats

# get_current_enemy 获得当前地图中全部的怪物的信息（包括伤害）
def get_current_enemy(map_data):
    temp_x = 0
    temp_y = 0
    height = int(HEIGHT / BLOCK_UNIT)
    width = int(WIDTH / BLOCK_UNIT) - 4 # -4是因为左边有状态栏
    enemy_list = []
    while temp_y < height:
        while temp_x < width:
            if map_data[temp_y][temp_x] > 200:
                if map_data[temp_y][temp_x] not in enemy_list:
                    enemy_list.append(map_data[temp_y][temp_x])
            temp_x += 1
        temp_y += 1
        temp_x = 0
    enemy_info_list = []
    for enemy in enemy_list:
        enemy_info = get_damage_info(enemy)
        enemy_info_list.append(enemy_info)
    return enemy_info_list

# battle 进行战斗并结算
def battle(map_object, x, y):
    result = get_damage_info(map_object)
    # 检测怪物是否无法被破防
    if result["status"] == False:
        return False
    # 检测玩家是否会被击杀
    else:
        # 如果受到伤害大于玩家血量，不触发战斗
        if result["damage"] >= PlayerCon.hp:
            return False
        else:
            # 战后勇士数据结算
            PlayerCon.hp -= result["damage"]
            PlayerCon.gold += result["mon_gold"]
            PlayerCon.exp += result["mon_exp"]
            # 将怪物从地图中删去
            CurrentMap.remove_block(x, y)
            flush_status()
            return True

# pickup_item 处理物品（直接使用/进入道具栏）
def pickup_item(map_object, x, y):
    item_name = BlockData[str(map_object)]["id"]
    item_type = ITEMS_DATA["items"][item_name]["cls"]
    # item_type为items，直接使用
    if item_type == "items":
        exec(ITEMS_DATA["itemEffect"][item_name])
        CurrentMap.remove_block(x, y)
        CurrentMap.draw_map()
    # item_type为constants/tools，进入道具栏
    elif item_type == "constants" or item_type == "tools":
        try:
            PlayerCon.item[map_object] += 1
        except KeyError:
            PlayerCon.item[map_object] = 1
        finally:
            CurrentMap.remove_block(x, y)
            CurrentMap.draw_map()
    # item_type为keys，直接在玩家属性添加（钥匙为玩家属性一部分）
    elif item_type == "keys":
        if map_object == 21:
            PlayerCon.yellowkey += 1
        elif map_object == 22:
            PlayerCon.bluekey += 1
        elif map_object == 23:
            PlayerCon.redkey += 1
        CurrentMap.remove_block(x, y)
        CurrentMap.draw_map()
    else:
        pass
    # 刷新状态栏显示
    draw_status_bar()

        
# open_door 处理开门事件（map_object = 85 -> 花门）
def open_door(map_object, x, y):
    if map_object == 81 and PlayerCon.yellowkey > 0:
        PlayerCon.yellowkey -= 1
        CurrentMap.remove_block(x, y)
        flush_status()
        return True
    elif map_object == 82 and PlayerCon.bluekey > 0:
        PlayerCon.bluekey -= 1
        CurrentMap.remove_block(x, y)
        flush_status()
        return True
    elif map_object == 83 and PlayerCon.redkey > 0:
        PlayerCon.redkey -= 1
        CurrentMap.remove_block(x, y)
        flush_status()
        return True
    elif map_object == 84 and PlayerCon.greenkey > 0:
        PlayerCon.greenkey -= 1
        CurrentMap.remove_block(x, y)
        flush_status()
        return True
    elif map_object == 86:
        if STEEL_DOOR_NEEDS_KEY:
            if PlayerCon.steelkey > 0:
                PlayerCon.steelkey -= 1
                CurrentMap.remove_block(x, y)
                flush_status()
                return True
        else:
            CurrentMap.remove_block(x, y)
            flush_status()
            return True
    return False

# change_floor 处理切换楼层
def change_floor(block, x, y):
    # 上楼处理
    if block == 87:
        CurrentMap.set_map(MAP_DATABASE[PlayerCon.floor + 1])
        PlayerCon.floor += 1
        check_map_result = CurrentMap.check_block(88)
        print(f"check_map_result:{check_map_result}")
        if len(check_map_result) == 1:
            x_coordinate = check_map_result[0][0]
            y_coordinate = check_map_result[0][1]
            PlayerCon.change_hero_loc(x_coordinate, y_coordinate)
    # 下楼处理
    elif block == 88:
        CurrentMap.set_map(MAP_DATABASE[PlayerCon.floor - 1])
        PlayerCon.floor -= 1
        check_map_result = CurrentMap.check_block(87)
        print(f"check_map_result:{check_map_result}")
        if len(check_map_result) == 1:
            x_coordinate = check_map_result[0][0]
            y_coordinate = check_map_result[0][1]
            PlayerCon.change_hero_loc(x_coordinate, y_coordinate)
    # TODO: 事件调用（不指定楼梯）
    flush_status()

# draw_status_bar 绘制状态栏（默认绘制在StatusBar图层）
def draw_status_bar(StatusBar=None):
    if StatusBar == None:
        StatusBar = global_var.get_value("StatusBar")
    StatusBar.fill(SKYBLUE)
    StatusBar.draw_text("FLOOR = " + str(PlayerCon.floor), 36, WHITE, 0, 0)
    StatusBar.draw_text("HP = " + str(PlayerCon.hp), 36, WHITE, 0, 1)
    StatusBar.draw_text("ATK = " + str(PlayerCon.attack), 36, WHITE, 0, 2)
    StatusBar.draw_text("DEF = " + str(PlayerCon.defend), 36, WHITE, 0, 3)
    StatusBar.draw_text("MDEF = " + str(PlayerCon.mdefend), 36, WHITE, 0, 4)
    StatusBar.draw_text("GOLD = " + str(PlayerCon.gold), 36, WHITE, 0, 5)
    StatusBar.draw_text("EXP = " + str(PlayerCon.exp), 36, WHITE, 0, 6)
    StatusBar.draw_text("Y_KEY = " + str(PlayerCon.yellowkey), 36, WHITE, 0, 7)
    StatusBar.draw_text("B_KEY = " + str(PlayerCon.bluekey), 36, WHITE, 0, 8)
    StatusBar.draw_text("R_KEY = " + str(PlayerCon.redkey), 36, WHITE, 0, 9)

# draw_start_menu 绘制开始菜单
# TODO: 文字居中自适应
def draw_start_menu(index=1):
    global_var.set_value("index",index)
    RootScreen.fill(SKYBLUE)
    RootScreen.draw_text(TOWER_NAME, 64, WHITE, 6, 0)
    RootScreen.draw_text("开始游戏", 36, WHITE, 7, 6)
    RootScreen.draw_text("读取存档", 36, WHITE, 7, 7)
    if index == 1:
        RootScreen.draw_text("->", 36, WHITE, 6, 6)
    if index == 2:
        RootScreen.draw_text("->", 36, WHITE, 6, 7)
    pygame.display.flip()
    

# wait_start_menu 在开始菜单页面等待并执行用户操作
def wait_start_menu():
    index = global_var.get_value("index")
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP and index > 1:
                    draw_start_menu(index-1)
                    index = global_var.get_value("index")
                elif event.key == pygame.K_DOWN and index < 2:
                    draw_start_menu(index+1)
                    index = global_var.get_value("index")
                elif event.key == pygame.K_RETURN and index == 1: # K_RETURN就是ENTER键
                    waiting = False
    print("GAME START!")
    

# draw_enemy_book 绘制怪物手册
def draw_enemy_book(current_index=0, map_index=None):
    if map_index == None:
        map_index = PlayerCon.floor
    # UI背景和左侧状态栏
    RootScreen.fill(SKYBLUE)
    draw_status_bar(RootScreen)
    # 获得当前地图中全部的怪物的信息
    enemy_info_list = get_current_enemy(MAP_DATABASE[map_index])
    # 如果当前楼层没有怪物
    if len(enemy_info_list) == 0:
        RootScreen.draw_text("本层无怪物", 72, BLACK, (17 * BLOCK_UNIT / 2) - (72 * 1.5), (13 * BLOCK_UNIT / 2) - 36, "px")
        global_var.set_value("index", current_index)
        pygame.display.update()
        return
    current_index = max(0, current_index)
    current_index = min(current_index, len(enemy_info_list) - 1)
    global_var.set_value("index", current_index)
    # 计算分页并从enemy_info_list中提取需要展示的数据
    item_per_page = 6
    total_page = math.ceil(len(enemy_info_list) / item_per_page)
    current_page = math.ceil((current_index + 1) / item_per_page)
    slice_start = (current_page - 1) * item_per_page
    slice_end = min(slice_start + 6, len(enemy_info_list))
    enemy_info_list = enemy_info_list[slice_start:slice_end]
    # 绘制怪物手册条目
    i = 0
    for enemy in enemy_info_list:
        RootScreen.draw_text(str(enemy["mon_name"]), 30, BLACK, 6 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10, "px")
        RootScreen.draw_text("生命 " + str(enemy["mon_hp"]), 30, BLACK, 8 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10, "px")
        RootScreen.draw_text("攻击 " + str(enemy["mon_atk"]), 30, BLACK, 11 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10, "px")
        RootScreen.draw_text("防御 " + str(enemy["mon_def"]), 30, BLACK, 14 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10, "px")
        RootScreen.draw_text("金币 " + str(enemy["mon_gold"]), 30, BLACK, 8 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 46, "px")
        RootScreen.draw_text("经验 " + str(enemy["mon_exp"]), 30, BLACK, 11 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 46, "px")
        RootScreen.draw_text("伤害 " + str(enemy["damage"]), 30, BLACK, 14 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 46, "px")
        RootScreen.draw_text("临界 " + "None", 30, BLACK, 8 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 82, "px")
        RootScreen.draw_text("减伤 " + "None", 30, BLACK, 11 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 82, "px")
        RootScreen.draw_text("1防 " + "None", 30, BLACK, 14 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 82, "px")
        i += 1
    # 根据当前current_index绘制高亮框
    i = current_index % item_per_page
    RootScreen.draw_rect((4 * BLOCK_UNIT, 2 * BLOCK_UNIT * i), (17 * BLOCK_UNIT - 10, 2 * BLOCK_UNIT * (i + 1)), 3, RED, "px")
    pygame.display.update()
    print(f"BOOK SHOW! Index = {current_index}")
    
# wait_enemy_book 在怪物手册页面等待并执行用户操作
def wait_enemy_book():
    index = global_var.get_value("index")
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    draw_enemy_book(index-1)
                    index = global_var.get_value("index")
                elif event.key == pygame.K_DOWN:
                    draw_enemy_book(index+1)
                    index = global_var.get_value("index")
                elif event.key == pygame.K_LEFT:
                    draw_enemy_book(index-6)
                    index = global_var.get_value("index")
                elif event.key == pygame.K_RIGHT:
                    draw_enemy_book(index+6)
                    index = global_var.get_value("index")
                elif event.key == pygame.K_ESCAPE:
                    waiting = False
    print("BOOK CLOSED!")
'''
# use_item can use a constant / tool item
def use_item(item_number):
    item_name = RELATIONSHIP_DICT[str(item_number)]["id"]
    results = exec(ITEM_PROPERTY["useItemEffect"][item_name])
    if results["result"] == False:
        print(results["msg"])  # Will put it in a msg box in the future

'''
