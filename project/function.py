import math

from lib import CurrentMap
from lib import ui
from project.enemy import *
from project.block import BlockData
from project.items import ITEMS_DATA
import lib
from project.floors import MAP_DATABASE

# get_damage_info 获取战斗伤害（模拟战斗）
def get_damage_info(map_object):
    # 通过get_monster_data获得怪物数据
    monster_stats = get_monster_data(map_object)
    mon_name = monster_stats["name"]
    mon_hp = monster_stats["hp"]
    mon_atk = monster_stats["atk"]
    mon_def = monster_stats["def"]
    mon_gold = monster_stats["money"]
    mon_exp = monster_stats["experience"]
    # 检测勇士能否破怪物防御
    if lib.PlayerCon.attack <= mon_def:
        return False
    # 计算每回合勇士受到的伤害
    damage_from_mon_per_turn = mon_atk - lib.PlayerCon.defend
    # 勇士受到伤害是否 < 0
    if damage_from_mon_per_turn < 0:
        damage_from_mon_per_turn = 0
    # 计算每回合勇士对怪物造成的伤害
    damage_from_hero_per_turn = lib.PlayerCon.attack - mon_def
    # 计算勇士击杀怪物所需的回合数
    turn = math.ceil(mon_hp / damage_from_hero_per_turn)
    # 计算勇士本次战斗所受到的伤害
    damage = damage_from_mon_per_turn * (turn - 1) - lib.PlayerCon.mdefend
    # 勇士不允许受到负数伤害（治疗）
    if damage < 0:
        damage = 0
    result = {"damage": damage, "mon_gold": mon_gold, "mon_exp": mon_exp}
    return result

# get_monster_data 获得怪物数据
def get_monster_data(map_object):
    # 从/project/block.py获取怪物id
    monster_id = BlockData[str(map_object)]["id"]
    # 从/project/enemy.py获取怪物详细数据
    monster_stats = MONSTER_DATA[monster_id]
    return monster_stats

# battle 进行战斗并结算
def battle(map_object, x, y):
    result = get_damage_info(map_object)
    # 检测怪物是否无法被破防
    if result == False:
        return False
    # 检测玩家是否会被击杀
    else:
        # 如果受到伤害大于玩家血量，不触发战斗
        if result["damage"] >= lib.PlayerCon.hp:
            return False
        else:
            # 战后勇士数据结算
            lib.PlayerCon.hp -= result["damage"]
            lib.PlayerCon.gold += result["mon_gold"]
            lib.PlayerCon.exp += result["mon_exp"]
            # 将怪物从地图中删去
            CurrentMap.set_block(x, y, 0)
            # 刷新地图显示
            CurrentMap.draw_map()
            # 刷新状态栏显示
            ui.update_status_bar()
            return True

# pickup_item 处理物品（直接使用/进入道具栏）
def pickup_item(map_object, x, y):
    item_name = BlockData[str(map_object)]["id"]
    item_type = ITEMS_DATA["items"][item_name]["cls"]
    # item_type为items，直接使用
    if item_type == "items":
        exec(ITEMS_DATA["itemEffect"][item_name])
        CurrentMap.set_block(x, y, 0)
        CurrentMap.draw_map()
    # item_type为constants/tools，进入道具栏
    elif item_type == "constants" or item_type == "tools":
        try:
            lib.PlayerCon.item[map_object] += 1
        except KeyError:
            lib.PlayerCon.item[map_object] = 1
        finally:
            CurrentMap.set_block(x, y, 0)
            CurrentMap.draw_map()
    # item_type为keys，直接在玩家属性添加（钥匙为玩家属性一部分）
    elif item_type == "keys":
        if map_object == 21:
            lib.PlayerCon.yellowkey += 1
        elif map_object == 22:
            lib.PlayerCon.bluekey += 1
        elif map_object == 23:
            lib.PlayerCon.redkey += 1
        CurrentMap.set_block(x, y, 0)
        CurrentMap.draw_map()
    else:
        pass
    # 刷新状态栏显示
    ui.update_status_bar()

        
# open_door 处理开门事件（map_object = 85 -> 花门）
def open_door(map_object, x, y):
    if map_object == 81 and lib.PlayerCon.yellowkey > 0:
        lib.PlayerCon.yellowkey -= 1
        CurrentMap.set_block(x, y, 0)
        # 刷新地图显示
        CurrentMap.draw_map()
        # 刷新状态栏显示
        ui.update_status_bar()
        return True
    elif map_object == 82 and lib.PlayerCon.bluekey > 0:
        lib.PlayerCon.bluekey -= 1
        CurrentMap.set_block(x, y, 0)
        # 刷新地图显示
        CurrentMap.draw_map()
        # 刷新状态栏显示
        ui.update_status_bar()
        return True
    elif map_object == 83 and lib.PlayerCon.redkey > 0:
        lib.PlayerCon.redkey -= 1
        CurrentMap.set_block(x, y, 0)
        # 刷新地图显示
        CurrentMap.draw_map()
        # 刷新状态栏显示
        ui.update_status_bar()
        return True
    elif map_object == 84 and lib.PlayerCon.greenkey > 0:
        lib.PlayerCon.greenkey -= 1
        CurrentMap.set_block(x, y, 0)
        # 刷新地图显示
        CurrentMap.draw_map()
        # 刷新状态栏显示
        ui.update_status_bar()
        return True
    elif map_object == 86:
        if STEEL_DOOR_NEEDS_KEY:
            if lib.PlayerCon.steelkey > 0:
                lib.PlayerCon.steelkey -= 1
                CurrentMap.set_block(x, y, 0)
                # 刷新地图显示
                CurrentMap.draw_map()
                # 刷新状态栏显示
                ui.update_status_bar()
                return True
        else:
            CurrentMap.set_block(x, y, 0)
            # 刷新地图显示
            CurrentMap.draw_map()
            # 刷新状态栏显示
            ui.update_status_bar()
            return True
    return False

# change_floor 处理切换楼层
def change_floor(block, x, y):
    # 上楼处理
    if block == 87:
        CurrentMap.set_map(MAP_DATABASE[lib.PlayerCon.floor + 1])
        lib.PlayerCon.floor += 1
        check_map_result = CurrentMap.check_block(88)
        print(f"check_map_result:{check_map_result}")
        if len(check_map_result) == 1:
            x_coordinate = check_map_result[0][0]
            y_coordinate = check_map_result[0][1]
            lib.PlayerCon.change_hero_loc(x_coordinate, y_coordinate)
    # 下楼处理
    elif block == 88:
        CurrentMap.set_map(MAP_DATABASE[lib.PlayerCon.floor - 1])
        lib.PlayerCon.floor -= 1
        check_map_result = CurrentMap.check_block(87)
        print(f"check_map_result:{check_map_result}")
        if len(check_map_result) == 1:
            x_coordinate = check_map_result[0][0]
            y_coordinate = check_map_result[0][1]
            lib.PlayerCon.change_hero_loc(x_coordinate, y_coordinate)
    # TODO: 事件调用（不指定楼梯）
    # 刷新地图显示
    CurrentMap.draw_map()
    # 刷新状态栏显示
    ui.update_status_bar()

'''
# use_item can use a constant / tool item
def use_item(item_number):
    item_name = RELATIONSHIP_DICT[str(item_number)]["id"]
    results = exec(ITEM_PROPERTY["useItemEffect"][item_name])
    if results["result"] == False:
        print(results["msg"])  # Will put it in a msg box in the future

'''
