import math
import pygame
from lib import CurrentMap
from project.enemy import *
from project.block import BlockData
from project.items import ITEMS_DATA
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
def get_damage_info(map_object,hero_atk=None,hero_def=None,hero_mdef=None):
    if hero_atk == None and hero_def == None and hero_mdef == None:
        hero_atk = PlayerCon.attack
        hero_def = PlayerCon.defend
        hero_mdef = PlayerCon.mdefend
    # 通过get_enemy_info获得怪物数据
    monster_stats = get_enemy_info(map_object)
    mon_name = monster_stats["name"]
    mon_hp = monster_stats["hp"]
    mon_atk = monster_stats["atk"]
    mon_def = monster_stats["def"]
    mon_gold = monster_stats["money"]
    mon_exp = monster_stats["experience"]
    # 检测勇士能否破怪物防御
    if hero_atk <= mon_def:
        return {"status": False,
                "mon_name": mon_name,
                "mon_hp": mon_hp,
                "mon_atk": mon_atk,
                "mon_def": mon_def,
                "mon_gold": mon_gold,
                "mon_exp": mon_exp,
                "damage": "???"}
    # 计算每回合勇士受到的伤害
    damage_from_mon_per_turn = mon_atk - hero_def
    # 勇士受到伤害是否 < 0
    if damage_from_mon_per_turn < 0:
        damage_from_mon_per_turn = 0
    # 计算每回合勇士对怪物造成的伤害
    damage_from_hero_per_turn = hero_atk - mon_def
    # 计算勇士击杀怪物所需的回合数
    turn = math.ceil(mon_hp / damage_from_hero_per_turn)
    # 计算勇士本次战斗所受到的伤害
    damage = damage_from_mon_per_turn * (turn - 1) - hero_mdef
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

# get_criticals 获得攻击临界数据
# map_object（怪物数字id），result_num（临界结果数量）
# TODO: 目前使用暴力循环法，未来实现二分法
def get_criticals(map_object, result_num):
    # 设定循环攻击上限
    LOOP_MAX_ATK = 100
    critical_list = []
    hero_atk = PlayerCon.attack
    hero_def = PlayerCon.defend
    hero_mdef = PlayerCon.mdefend
    # 获得当前怪物伤害数据
    monster_stats = get_enemy_info(map_object)
    initial_damage_info = get_damage_info(map_object)
    previous_damage = initial_damage_info["damage"]
    # 如果无法破防，直接返回破防所需的增量攻击
    if previous_damage == "???":
        return [[initial_damage_info["mon_def"] - hero_atk + 1, "???"]]
    if hero_atk <= LOOP_MAX_ATK:
        for new_atk in range(hero_atk+1, monster_stats["hp"] + monster_stats["def"]):
            next_damage_info = get_damage_info(map_object,new_atk,hero_def,hero_mdef)
            next_damage = next_damage_info["damage"]
            if next_damage < previous_damage:
                previous_damage = next_damage
                critical_list.append([new_atk - hero_atk, initial_damage_info["damage"] - next_damage])
                # 如果出现无伤或者记录了足够数量的临界点，就停止计算
                # TODO: 负伤害处理？？
                if next_damage <= 0 or len(critical_list) >= result_num:
                    break
        return critical_list
    else:
        return []


# next_def_critical 获得防御临界数据
def next_def_critical(map_object):
    original_damage = get_damage_info(map_object)
    next_def_damage = get_damage_info(map_object, PlayerCon.attack, PlayerCon.defend + 1, PlayerCon.mdefend)
    if original_damage["damage"] != "???" and next_def_damage["damage"] != "???":
        return original_damage["damage"] - next_def_damage["damage"]
    else:
        return "???"
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
        # 获取怪物战斗伤害和基本信息
        enemy_info = get_damage_info(enemy)
        # 往enemy_info写入怪物数字id
        enemy_info["mon_num_id"] = enemy
        # 获取攻击临界点（此处返回数组长度最大为3）
        critical_info = get_criticals(enemy, 3)
        if len(critical_info) > 0:
            enemy_info["next_critical"] = critical_info[0][0]
            enemy_info["next_critical_decrease"] = critical_info[0][1]
        else:
            enemy_info["next_critical"] = 0
            enemy_info["next_critical_decrease"] = 0
        # 获取防御临界点
        enemy_info["next_def_critical"] = next_def_critical(enemy)
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

# pickup_item 玩家捡起物品（直接使用/进入道具栏）
def pickup_item(map_object, x, y):
    item_name = BlockData[str(map_object)]["id"]
    item_type = ITEMS_DATA["items"][item_name]["cls"]
    # item_type为items，直接使用
    if item_type == "items":
        exec(ITEMS_DATA["itemEffect"][item_name])
        CurrentMap.remove_block(x, y)
        flush_status()
    # item_type为constants/tools/keys，进入道具栏
    elif item_type == "constants" or item_type == "tools" or item_type == "keys":
        if map_object in PlayerCon.item:
            PlayerCon.item[map_object] += 1
        else:
            PlayerCon.item[map_object] = 1
        CurrentMap.remove_block(x, y)
        flush_status()
    else:
        pass
    # 刷新状态栏显示
    draw_status_bar()

# remove_item 从背包移除物品
def remove_item(map_object, amount):
    # 判断玩家是否拥有该物品
    if map_object in PlayerCon.item:
        # 判断玩家是否拥有足够数量的物品被移除
        if amount < PlayerCon.item[map_object]:
            # 玩家拥有足量物品，那么移除指定数量
            PlayerCon.item[map_object] -= amount
        else:
            # 玩家没有足量物品，直接对该物品进行清零
            PlayerCon.item.pop(map_object)

# add_item 向背包增加物品
def add_item(map_object, amount):
    if map_object in PlayerCon.item:
        PlayerCon.item[map_object] += amount
    else:
        PlayerCon.item[map_object] = amount

# count_item 获取背包中指定物品的数量
def count_item(map_object):
    if map_object in PlayerCon.item:
        return PlayerCon.item[map_object]
    else:
        return 0

# sort_item 将玩家当前持有物品分类，传入类别字典，返回字典
# 数据结构：sort_info[道具类别][道具数字id][道具各种详细信息]
def sort_item(category):
    sort_info = category
    for key in sort_info:
        sort_info[key] = {}
    for item in PlayerCon.item:
        item_id = BlockData[str(item)]["id"]
        item_cls = ITEMS_DATA["items"][item_id]["cls"]
        if item_cls in category:
            item_name = ITEMS_DATA["items"][item_id]["name"]
            if "text" in ITEMS_DATA["items"][item_id]:
                item_text = ITEMS_DATA["items"][item_id]["text"]
            else:
                item_text = "本物品暂时没有描述"
            item_amount = count_item(item)
            sort_info[item_cls][item] = {}
            sort_info[item_cls][item]["item_id"] = item_id
            sort_info[item_cls][item]["item_name"] = item_name
            sort_info[item_cls][item]["item_text"] = item_text
            sort_info[item_cls][item]["item_amount"] = item_amount
    return sort_info
            
# open_door 处理开门事件
def open_door(map_object, x, y, no_key=False):
    # 定义门与钥匙对应关系，默认花门（map_object=85）无法通过钥匙打开
    door_to_key = {81: 21,
                   82: 22,
                   83: 23,
                   84: 24,
                   86: 25}
    # 如果无需钥匙，直接开门
    if no_key:
        CurrentMap.remove_block(x, y)
        flush_status()
        return True
    # 如果是铁门而且无需钥匙，直接开门
    if map_object == 86 and STEEL_DOOR_NEEDS_KEY == False:
        CurrentMap.remove_block(x, y)
        flush_status()
        return True
    # 从door_to_key找出门对应的钥匙，找不到代表不能用钥匙开
    if map_object in door_to_key:
        key = door_to_key[map_object]
    else:
        return False
    # 如果玩家持有钥匙，那么扣除钥匙开门
    if key in PlayerCon.item:
        if PlayerCon.item[key] > 1:
            PlayerCon.item[key] -= 1
        else:
            PlayerCon.item.pop(key)
        CurrentMap.remove_block(x, y)
        flush_status()
        return True
    return False

# change_floor 处理切换楼层
def change_floor(block, x, y):
    MAP_DATABASE = global_var.get_value("MAP_DATABASE")
    floor_index = global_var.get_value("floor_index")
    # 上楼处理
    if block == 87:
        PlayerCon.floor += 1
        CurrentMap.set_map(PlayerCon.floor)
        check_map_result = CurrentMap.check_block(88)
        print(f"check_map_result:{check_map_result}")
        if len(check_map_result) == 1:
            x_coordinate = check_map_result[0][0]
            y_coordinate = check_map_result[0][1]
            PlayerCon.change_hero_loc(x_coordinate, y_coordinate)
    # 下楼处理
    elif block == 88:
        PlayerCon.floor -= 1
        CurrentMap.set_map(PlayerCon.floor)
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
    if 21 in PlayerCon.item:
        yellowkey = PlayerCon.item[21]
    else:
        yellowkey = 0
    if 22 in PlayerCon.item:
        bluekey = PlayerCon.item[22]
    else:
        bluekey = 0
    if 23 in PlayerCon.item:
        redkey = PlayerCon.item[23]
    else:
        redkey = 0
    StatusBar.fill(SKYBLUE)
    StatusBar.draw_text("FLOOR = " + str(PlayerCon.floor), 36, BLACK, 0, 0)
    StatusBar.draw_text("HP = " + str(PlayerCon.hp), 36, BLACK, 0, 1)
    StatusBar.draw_text("ATK = " + str(PlayerCon.attack), 36, BLACK, 0, 2)
    StatusBar.draw_text("DEF = " + str(PlayerCon.defend), 36, BLACK, 0, 3)
    StatusBar.draw_text("MDEF = " + str(PlayerCon.mdefend), 36, BLACK, 0, 4)
    StatusBar.draw_text("GOLD = " + str(PlayerCon.gold), 36, BLACK, 0, 5)
    StatusBar.draw_text("EXP = " + str(PlayerCon.exp), 36, BLACK, 0, 6)
    StatusBar.draw_text("Y_KEY = " + str(yellowkey), 36, BLACK, 0, 7)
    StatusBar.draw_text("B_KEY = " + str(bluekey), 36, BLACK, 0, 8)
    StatusBar.draw_text("R_KEY = " + str(redkey), 36, BLACK, 0, 9)


'''
# use_item can use a constant / tool item
def use_item(item_number):
    item_name = RELATIONSHIP_DICT[str(item_number)]["id"]
    results = exec(ITEM_PROPERTY["useItemEffect"][item_name])
    if results["result"] == False:
        print(results["msg"])  # Will put it in a msg box in the future

'''
