import math

from lib import CurrentMap
from lib import ui
from project.enemy import *
from project.block import *
from project.items import ITEMS_DATA
import lib

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

# pickup_item can process item pick up events
def pickup_item(map_object, x, y):
    item_name = BlockData[str(map_object)]["id"]
    item_type = ITEMS_DATA["items"][item_name]["cls"]
    if item_type == "items":
        exec(ITEMS_DATA["itemEffect"][item_name])
        CurrentMap.set_block(x, y, 0)
        CurrentMap.draw_map()
        # 刷新状态栏显示
        ui.update_status_bar()
    elif item_type == "constants" or item_type == "tools":
        try:
            lib.PlayerCon.item[map_object] += 1
        except KeyError:
            lib.PlayerCon.item[map_object] = 1
        finally:
            CurrentMap.set_block(x, y, 0)
            CurrentMap.draw_map()
            # 刷新状态栏显示
            ui.update_status_bar()
    else:
        pass

'''
# Events functions
# detect_events determine the event function that should be triggered
def detect_events(map_object, row, column):
    # According to HTML5 Magic Tower,
    # 0 = Nothing (No obstacle)
    # 1 = Wall (blocks the player)
    # 21 - 69 = Items (Player can step on it and get the item)
    # 81 - 86 = Doors (player can't step on but instead open it)
    # 87 - 88 = Stairs (Player can't step on it)
    # 201+ = Monsters (trigger battle)
    if map_object == 0:
        return True
    else:
        if map_object == 1:
            return False
        elif map_object >= 21 and map_object <= 69:
            pickup_item(map_object, row, column)
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


# use_item can use a constant / tool item
def use_item(item_number):
    item_name = RELATIONSHIP_DICT[str(item_number)]["id"]
    results = exec(ITEM_PROPERTY["useItemEffect"][item_name])
    if results["result"] == False:
        print(results["msg"])  # Will put it in a msg box in the future


# open_door can open the door if requirements are met
def open_door(map_object, column, row):
    if map_object == 81 and player.yellowkey > 0:
        player.yellowkey -= 1
        map_write(player.floor, column, row, 0)
    elif map_object == 82 and player.bluekey > 0:
        player.bluekey -= 1
        map_write(player.floor, column, row, 0)
    elif map_object == 83 and player.redkey > 0:
        player.redkey -= 1
        map_write(player.floor, column, row, 0)
    elif map_object == 84 and player.greenkey > 0:
        player.greenkey -= 1
        map_write(player.floor, column, row, 0)
    elif map_object == 85:
        map_write(player.floor, column, row, 0)
    elif map_object == 86:
        if STEEL_DOOR_NEEDS_KEY:
            if player.steelkey > 0:
                player.steelkey -= 1
                map_write(player.floor, column, row, 0)
        else:
            map_write(player.floor, column, row, 0)


# Change floor can change the floor and it can be used without a stair
# change_floor(destination floor, x, y)
def change_floor(floor, column, row):
    if floor == "go_upstairs":
        check_map_result = check_map(player.floor + 1, 88)
        print(check_map_result)
        if check_map_result["result"]:
            x_coordinate = check_map_result["x_coordinate"]
            y_coordinate = check_map_result["y_coordinate"]
            player.move_directly([x_coordinate, y_coordinate])
        player.floor += 1
    elif floor == "go_downstairs":
        check_map_result = check_map(player.floor - 1, 87)
        if check_map_result["result"]:
            x_coordinate = check_map_result["x_coordinate"]
            y_coordinate = check_map_result["y_coordinate"]
            player.move_directly([x_coordinate, y_coordinate])
        player.floor -= 1
    # When this function is not triggered by stairs
    else:
        x_coordinate = column
        y_coordinate = row
        player.move_directly([x_coordinate, y_coordinate])
        player.floor = floor

'''
