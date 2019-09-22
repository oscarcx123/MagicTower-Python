import math
import pygame
from lib import global_var
from sysconf import *


class Function():
    def __init__(self):
        pass

    def init_var(self):
        from project.enemy import MONSTER_DATA
        from project.block import BlockData
        from project.items import ITEMS_DATA
        self.PlayerCon = global_var.get_value("PlayerCon")
        self.RootScreen = global_var.get_value("RootScreen")
        self.CurrentMap = global_var.get_value("CurrentMap")
        self.Music = global_var.get_value("Music")
        self.StatusBar = global_var.get_value("StatusBar")
        self.MONSTER_DATA = MONSTER_DATA
        self.BlockData = BlockData
        self.ITEMS_DATA = ITEMS_DATA

    # flush_status 刷新地图&状态栏显示
    def flush_status(self):
        # 刷新地图显示
        self.CurrentMap.draw_map()
        # 刷新状态栏显示
        self.draw_status_bar()

    # 检测怪物是否有指定特殊能力
    def has_ability(self, mon_ability, ability_num):
        if type(mon_ability) is int:
            if ability_num == mon_ability:
                return True
            else:
                return False
        else:
            if ability_num in mon_ability:
                return True
            else:
                return False


    # get_damage_info 获取战斗伤害（模拟战斗）
    def get_damage_info(self, map_object,hero_atk=None,hero_def=None,hero_mdef=None):
        # 勇士可以对怪物造成伤害的情况
        def return_good():
            return {"status": True,
                    "mon_name": mon_name,
                    "mon_hp": mon_hp,
                    "mon_atk": mon_atk,
                    "mon_def": mon_def,
                    "mon_gold": mon_gold,
                    "mon_exp": mon_exp,
                    "damage": damage,
                    "mon_ability": mon_ability}
        
        # 勇士无法对怪物造成伤害
        def return_bad():
            return {"status": False,
                    "mon_name": mon_name,
                    "mon_hp": mon_hp,
                    "mon_atk": mon_atk,
                    "mon_def": mon_def,
                    "mon_gold": mon_gold,
                    "mon_exp": mon_exp,
                    "damage": "???",
                    "mon_ability": mon_ability}
        
        if hero_atk == None and hero_def == None and hero_mdef == None:
            hero_atk = self.PlayerCon.attack
            hero_def = self.PlayerCon.defend
            hero_mdef = self.PlayerCon.mdefend
        
        hero_hp = self.PlayerCon.hp
        
        # 通过get_enemy_info获得怪物数据
        monster_stats = self.get_enemy_info(map_object)
        mon_name = monster_stats["name"]
        mon_hp = monster_stats["hp"]
        mon_atk = monster_stats["atk"]
        mon_def = monster_stats["def"]
        mon_gold = monster_stats["money"]
        mon_exp = monster_stats["experience"]
        mon_ability = monster_stats["special"]

        # 初始化一些辅助计算数值
        # 初始伤害（战前额外伤害，先攻等等都使用这个计算）
        init_damage = 0
        # 单回合反击伤害（反击使用这个计算）
        counter_damage = 0

        # 检测勇士能否破怪物防御
        if hero_atk <= mon_def:
            return return_bad()

        # 无敌（勇士无法打败怪物，除非拥有十字架（id=55））
        if self.has_ability(mon_ability, 20) and self.has_item(55):
            return return_bad()

        # 吸血（战斗前，怪物首先吸取角色的%生命，根据add的值决定是否加到怪物身上）
        if self.has_ability(mon_ability, 11):
            try:
                vampire_rate = monster_stats["value"]
            except:
                vampire_rate = 0.2
            vampire_damage = math.floor(hero_hp * vampire_rate)
            try:
                vampire_add = monster_stats["add"]
            except:
                vampire_add = False
            if vampire_add:
                mon_hp += vampire_damage
            init_damage += vampire_damage

        # 计算每回合怪物对勇士造成的伤害
        damage_from_mon_per_turn = mon_atk - hero_def

        # 魔攻检测（怪物无视勇士的防御）
        if self.has_ability(mon_ability, 2):
            damage_from_mon_per_turn = mon_atk

        # 勇士受到伤害是否 < 0
        if damage_from_mon_per_turn < 0:
            damage_from_mon_per_turn = 0

        # 2连击（怪物每回合攻击2次）
        if self.has_ability(mon_ability, 4):
            damage_from_mon_per_turn *= 2

        # 3连击（怪物每回合攻击3次）
        if self.has_ability(mon_ability, 5):
            damage_from_mon_per_turn *= 3

        # N连击（怪物每回合攻击N次）
        if self.has_ability(mon_ability, 6):
            try:
                attack_count = monster_stats["n"]
            except:
                attack_count = 4
            damage_from_mon_per_turn *= attack_count

        # 反击（战斗时，怪物每回合附加角色攻击的counterAttack%作为伤害，无视角色防御）
        # 每回合的反击伤害；反击是按照勇士的攻击次数来计算回合
        if self.has_ability(mon_ability, 8):
            counter_damage += math.floor(MON_ABILITY_VALUE["counterAttack"] * hero_atk)

        # 先攻（怪物首先攻击）
        if self.has_ability(mon_ability, 1):
            init_damage += damage_from_mon_per_turn

        # 破甲（战斗前，怪物附加角色防御的breakArmor%作为伤害）
        if self.has_ability(mon_ability, 7):
            init_damage += math.floor(MON_ABILITY_VALUE["breakArmor"] * hero_def)

        # 净化（战斗前，怪物附加勇士魔防的purify倍作为伤害）
        if self.has_ability(mon_ability, 9):
            init_damage += math.floor(MON_ABILITY_VALUE["purify"] * hero_mdef)

        # 计算每回合勇士对怪物造成的伤害
        damage_from_hero_per_turn = hero_atk - mon_def
        # 计算勇士击杀怪物所需的回合数
        turn = math.ceil(mon_hp / damage_from_hero_per_turn)
        # 计算勇士本次战斗所受到的伤害
        damage = init_damage + damage_from_mon_per_turn * (turn - 1) + counter_damage * turn - hero_mdef
        # 勇士不允许受到负数伤害（治疗）
        if damage < 0:
            damage = 0
        # 计算一些不可被魔法抵消的伤害
        # 固伤（战斗前，怪物对勇士造成damage点固定伤害，无视勇士魔防）
        if self.has_ability(mon_ability, 22):
            try:
                extra_damage = monster_stats["damage"]
            except:
                print("获取怪物的固伤数值（damage）错误！")
                extra_damage = 10
            damage += extra_damage

        return return_good()

    # get_criticals 获得攻击临界数据
    # map_object（怪物数字id），result_num（临界结果数量）
    # TODO: 目前使用暴力循环法，未来实现二分法
    def get_criticals(self, map_object, result_num):
        # 设定循环攻击上限
        LOOP_MAX_ATK = 100
        critical_list = []
        hero_atk = self.PlayerCon.attack
        hero_def = self.PlayerCon.defend
        hero_mdef = self.PlayerCon.mdefend
        # 获得当前怪物伤害数据
        monster_stats = self.get_enemy_info(map_object)
        initial_damage_info = self.get_damage_info(map_object)
        previous_damage = initial_damage_info["damage"]
        # 如果无法破防，直接返回破防所需的增量攻击
        if previous_damage == "???":
            return [[initial_damage_info["mon_def"] - hero_atk + 1, "???"]]
        if hero_atk <= LOOP_MAX_ATK:
            for new_atk in range(hero_atk+1, monster_stats["hp"] + monster_stats["def"]):
                next_damage_info = self.get_damage_info(map_object,new_atk,hero_def,hero_mdef)
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
    def next_def_critical(self, map_object):
        original_damage = self.get_damage_info(map_object)
        next_def_damage = self.get_damage_info(map_object, self.PlayerCon.attack, self.PlayerCon.defend + 1, self.PlayerCon.mdefend)
        if original_damage["damage"] != "???" and next_def_damage["damage"] != "???":
            return original_damage["damage"] - next_def_damage["damage"]
        else:
            return "???"


    # get_enemy_info 获得怪物数据
    def get_enemy_info(self, map_object):
        # 从/project/block.py获取怪物id
        monster_id = self.BlockData[str(map_object)]["id"]
        # 从/project/enemy.py获取怪物详细数据
        monster_stats = self.MONSTER_DATA[monster_id]
        mon_ability = monster_stats["special"]

        # 模仿（怪物的攻防和勇士攻防相等）
        if self.has_ability(mon_ability, 10):
            monster_stats["atk"] = self.PlayerCon.attack
            monster_stats["def"] = self.PlayerCon.defend

        # 坚固（勇士每回合最多只能对怪物造成1点伤害）
        if self.has_ability(mon_ability, 3) and monster_stats["def"] < self.PlayerCon.attack - 1:
            monster_stats["def"] = self.PlayerCon.attack - 1

        return monster_stats

    # get_current_enemy 获得当前地图中全部的怪物的信息（包括伤害）
    def get_current_enemy(self, map_data):
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
        strong_enemy_info_list = []
        for enemy in enemy_list:
            # 获取怪物战斗伤害和基本信息
            enemy_info = self.get_damage_info(enemy)
            # 往enemy_info写入怪物数字id
            enemy_info["mon_num_id"] = enemy
            # 获取攻击临界点（此处返回数组长度最大为3）
            critical_info = self.get_criticals(enemy, 3)
            if len(critical_info) > 0:
                enemy_info["next_critical"] = critical_info[0][0]
                enemy_info["next_critical_decrease"] = critical_info[0][1]
            else:
                enemy_info["next_critical"] = 0
                enemy_info["next_critical_decrease"] = 0
            # 获取防御临界点
            enemy_info["next_def_critical"] = self.next_def_critical(enemy)
            if enemy_info["damage"] == "???":
                strong_enemy_info_list.append(enemy_info)
            else:
                enemy_info_list.append(enemy_info)
        enemy_info_list = sorted(enemy_info_list, key = lambda i: i["damage"])
        for enemy_info in strong_enemy_info_list:
            enemy_info_list.append(enemy_info)
        return enemy_info_list

    # battle 进行战斗并结算
    def battle(self, map_object, x, y):
        result = self.get_damage_info(map_object)
        # 检测怪物是否无法被破防
        if result["status"] == False:
            return False
        # 检测玩家是否会被击杀
        else:
            # 如果受到伤害大于玩家血量，不触发战斗
            if result["damage"] >= self.PlayerCon.hp:
                return False
            else:
                # 播放战斗音效
                self.Music.play_SE("attack.ogg")
                
                # 战后勇士数据结算
                self.PlayerCon.hp -= result["damage"]
                self.PlayerCon.gold += result["mon_gold"]
                self.PlayerCon.exp += result["mon_exp"]

                # 战后生效的怪物属性处理
                # 获取怪物数据用于处理战后生效的属性
                monster_id = self.BlockData[str(map_object)]["id"]
                monster_stats = self.MONSTER_DATA[monster_id]
                mon_ability = monster_stats["special"]

                # TODO:中毒


                # TODO:衰弱


                # TODO:诅咒


                # TODO:仇恨（击杀仇恨怪物，仇恨值减半）


                # 自爆（战斗后勇士的生命值变成1）
                if self.has_ability(mon_ability, 19):
                    self.PlayerCon.hp = 1

                # 退化
                if self.has_ability(mon_ability, 21):
                    try:
                        atkValue = monster_stats["atkValue"]
                    except:
                        print("退化怪物未设置atkValue！")
                        atkValue = 1
                    try:
                        defValue = monster_stats["defValue"]
                    except:
                        print("退化怪物未设置defValue！")
                        defValue = 1
                    self.PlayerCon.attack -= atkValue
                    self.PlayerCon.defend -= defValue
                    if self.PlayerCon.attack < 0:
                        self.PlayerCon.attack = 0
                    if self.PlayerCon.defend < 0:
                        self.PlayerCon.defend = 0

                # TODO:增加仇恨值


                # TODO:战后技能处理


                # TODO:加点



                # 将怪物从地图中删去
                self.CurrentMap.remove_block(x, y)
                self.flush_status()
                return True

    # pickup_item 玩家捡起物品（直接使用/进入道具栏）
    def pickup_item(self, map_object, x, y):
        self.Music.play_SE("item.ogg")
        item_name = self.BlockData[str(map_object)]["id"]
        item_type = self.ITEMS_DATA["items"][item_name]["cls"]
        # item_type为items，直接使用
        if item_type == "items":
            exec(self.ITEMS_DATA["itemEffect"][item_name])
            self.CurrentMap.remove_block(x, y)
            self.flush_status()
        # item_type为constants/tools/keys，进入道具栏
        elif item_type == "constants" or item_type == "tools" or item_type == "keys":
            if map_object in self.PlayerCon.item:
                self.PlayerCon.item[map_object] += 1
            else:
                self.PlayerCon.item[map_object] = 1
            self.CurrentMap.remove_block(x, y)
            self.flush_status()
        else:
            pass
        # 刷新状态栏显示
        self.draw_status_bar()

    # remove_item 从背包移除物品
    def remove_item(self, map_object, amount):
        # 判断玩家是否拥有该物品
        if map_object in self.PlayerCon.item:
            # 判断玩家是否拥有足够数量的物品被移除
            if amount < self.PlayerCon.item[map_object]:
                # 玩家拥有足量物品，那么移除指定数量
                self.PlayerCon.item[map_object] -= amount
            else:
                # 玩家没有足量物品，直接对该物品进行清零
                self.PlayerCon.item.pop(map_object)

    # add_item 向背包增加物品
    def add_item(self, map_object, amount):
        if map_object in self.PlayerCon.item:
            self.PlayerCon.item[map_object] += amount
        else:
            self.PlayerCon.item[map_object] = amount

    # set_item_amount 向背包增加物品
    def set_item_amount(self, map_object, amount):
        self.PlayerCon.item[map_object] = amount

    # count_item 获取背包中指定物品的数量
    def count_item(self, map_object):
        if type(map_object) is not int:
            BlockDataReverse = global_var.get_value("BlockDataReverse")
            map_object = int(BlockDataReverse[map_object])
        if map_object in self.PlayerCon.item:
            return self.PlayerCon.item[map_object]
        else:
            return 0

    # has_item 检测背包中是否有指定物品
    def has_item(self, map_object):
        if map_object in self.PlayerCon.item:
            return True
        else:
            return False

    # sort_item 将玩家当前持有物品分类，传入类别字典，返回字典
    # 数据结构：sort_info[道具类别][道具数字id][道具各种详细信息]
    def sort_item(self, category):
        sort_info = category
        for key in sort_info:
            sort_info[key] = {}
        for item in self.PlayerCon.item:
            item_id = self.BlockData[str(item)]["id"]
            item_cls = self.ITEMS_DATA["items"][item_id]["cls"]
            if item_cls in category:
                item_name = self.ITEMS_DATA["items"][item_id]["name"]
                if "text" in self.ITEMS_DATA["items"][item_id]:
                    item_text = self.ITEMS_DATA["items"][item_id]["text"]
                else:
                    item_text = "本物品暂时没有描述"
                item_amount = self.count_item(item)
                sort_info[item_cls][item] = {}
                sort_info[item_cls][item]["item_id"] = item_id
                sort_info[item_cls][item]["item_name"] = item_name
                sort_info[item_cls][item]["item_text"] = item_text
                sort_info[item_cls][item]["item_amount"] = item_amount
        return sort_info
            
    # open_door 处理开门事件
    def open_door(self, map_object, x, y, no_key=False):
        # 定义门与钥匙对应关系，默认花门（map_object=85）无法通过钥匙打开
        door_to_key = {81: 21,
                    82: 22,
                    83: 23,
                    84: 24,
                    86: 25}
        # ”无需钥匙“或者”是铁门而且无需钥匙“，直接开门
        if no_key or (map_object == 86 and STEEL_DOOR_NEEDS_KEY == False):
            self.Music.play_SE("door.ogg")
            self.CurrentMap.remove_block(x, y)
            self.flush_status()
            return True
        # 从door_to_key找出门对应的钥匙，找不到代表不能用钥匙开
        if map_object in door_to_key:
            key = door_to_key[map_object]
        else:
            return False
        # 如果玩家持有钥匙，那么扣除钥匙开门
        if key in self.PlayerCon.item:
            self.Music.play_SE("door.ogg")
            if self.PlayerCon.item[key] > 1:
                self.PlayerCon.item[key] -= 1
            else:
                self.PlayerCon.item.pop(key)
            self.CurrentMap.remove_block(x, y)
            self.flush_status()
            return True
        return False

    # change_floor 处理切换楼层
    def change_floor(self, block, floor=None, loc=None):
        # 使用楼层传送器，直接递归调用change_floor
        if block == "fly":
            if floor >= self.PlayerCon.floor:
                self.change_floor(87, floor=floor)
            elif floor < self.PlayerCon.floor:
                self.change_floor(88, floor=floor)
            return True

        MAP_DATABASE = global_var.get_value("MAP_DATABASE")
        floor_index = global_var.get_value("floor_index")
        self.Music.play_SE("floor.ogg")
        
        # 上楼处理
        if block == 87:
            if floor is not None:
                self.PlayerCon.floor = floor
            else:
                self.PlayerCon.floor += 1
            self.CurrentMap.set_map(self.PlayerCon.floor)
            check_map_result = self.CurrentMap.check_block(88)
            print(f"check_map_result:{check_map_result}")
            if len(check_map_result) == 1:
                x_coordinate = check_map_result[0][0]
                y_coordinate = check_map_result[0][1]
                self.PlayerCon.change_hero_loc(x_coordinate, y_coordinate)
        
        # 下楼处理
        elif block == 88:
            if floor is not None:
                self.PlayerCon.floor = floor
            else:
                self.PlayerCon.floor -= 1
            self.CurrentMap.set_map(self.PlayerCon.floor)
            check_map_result = self.CurrentMap.check_block(87)
            print(f"check_map_result:{check_map_result}")
            if len(check_map_result) == 1:
                x_coordinate = check_map_result[0][0]
                y_coordinate = check_map_result[0][1]
                self.PlayerCon.change_hero_loc(x_coordinate, y_coordinate)

        # 事件调用（不通过楼梯触发）
        else:
            if floor != None:
                self.PlayerCon.floor = floor
                self.CurrentMap.set_map(self.PlayerCon.floor)
            if loc != None:
                self.PlayerCon.change_hero_loc(loc[0], loc[1])

        # 切换BGM
        self.Music.change_BGM(self.PlayerCon.floor)
        
        # 检查玩家是否去过目标楼层
        if self.CurrentMap.floor_index["index"][self.PlayerCon.floor] not in self.PlayerCon.visited:
            self.PlayerCon.visited.append(self.CurrentMap.floor_index["index"][self.PlayerCon.floor])
        self.flush_status()

    # draw_status_bar 绘制状态栏（默认绘制在StatusBar图层）
    def draw_status_bar(self, StatusBar=None):
        if StatusBar == None:
            self.StatusBar = global_var.get_value("StatusBar")
        if 21 in self.PlayerCon.item:
            yellowkey = self.PlayerCon.item[21]
        else:
            yellowkey = 0
        if 22 in self.PlayerCon.item:
            bluekey = self.PlayerCon.item[22]
        else:
            bluekey = 0
        if 23 in self.PlayerCon.item:
            redkey = self.PlayerCon.item[23]
        else:
            redkey = 0
        self.StatusBar.fill(SKYBLUE)
        self.StatusBar.draw_text("FLOOR = " + str(self.PlayerCon.floor), 36, BLACK, 0, 0)
        self.StatusBar.draw_text("HP = " + str(self.PlayerCon.hp), 36, BLACK, 0, 1)
        self.StatusBar.draw_text("ATK = " + str(self.PlayerCon.attack), 36, BLACK, 0, 2)
        self.StatusBar.draw_text("DEF = " + str(self.PlayerCon.defend), 36, BLACK, 0, 3)
        self.StatusBar.draw_text("MDEF = " + str(self.PlayerCon.mdefend), 36, BLACK, 0, 4)
        self.StatusBar.draw_text("GOLD = " + str(self.PlayerCon.gold), 36, BLACK, 0, 5)
        self.StatusBar.draw_text("EXP = " + str(self.PlayerCon.exp), 36, BLACK, 0, 6)
        self.StatusBar.draw_text("Y_KEY = " + str(yellowkey), 36, BLACK, 0, 7)
        self.StatusBar.draw_text("B_KEY = " + str(bluekey), 36, BLACK, 0, 8)
        self.StatusBar.draw_text("R_KEY = " + str(redkey), 36, BLACK, 0, 9)

    # 获取怪物特殊能力的相关文字
    def get_ability_text(self, mon_ability):
        check_result = {}
        ability_dict = {
            1:["先攻", "怪物首先攻击"],
            2:["魔攻", "怪物无视勇士的防御"],
            3:["坚固", "勇士每回合最多只能对怪物造成1点伤害"],
            4:["2连击", "怪物每回合攻击2次"],
            5:["3连击", "怪物每回合攻击3次"],
            6:["N连击", "怪物每回合攻击N次"],
            7:["破甲", "战斗前，怪物附加角色防御的X%作为伤害"],
            8:["反击", "战斗时，怪物每回合附加角色攻击的X%作为伤害，无视角色防御"],
            9:["净化", "战斗前，怪物附加勇士魔防的X倍作为伤害"],
            10:["模仿", "怪物的攻防和勇士攻防相等"],
            11:["吸血", "战斗前，怪物首先吸取角色的X%生命（约X点）作为伤害，并把伤害数值加到自身生命上"],
            12:["中毒", "战斗后，勇士陷入中毒状态，每一步损失生命X点"],
            13:["衰弱", "战斗后，勇士陷入衰弱状态，攻防暂时下降X点 / X%"],
            14:["诅咒", "战斗后，勇士陷入诅咒状态，战斗无法获得金币和经验"],
            15:["领域", "经过怪物周围自动减生命X点"],
            16:["夹击", "经过两只相同的怪物中间，勇士生命值变成一半"],
            17:["仇恨", "战斗前，怪物附加之前积累的仇恨值作为伤害"],
            18:["阻击", "经过怪物的十字领域时自动减生命X点，同时怪物后退一格"],
            19:["自爆", "战斗后勇士的生命值变成1"],
            20:["无敌", "勇士无法打败怪物，除非拥有十字架"],
            21:["退化", "战斗后勇士永久下降X点攻击和X点防御"],
            22:["固伤", "战斗前，怪物对勇士造成X点固定伤害，无视勇士魔防。"],
            23:["重生", "怪物被击败后，角色转换楼层则怪物将再次出现"],
            24:["激光", "经过怪物同行或同列时自动减生命X点"],
            25:["光环", "同楼层所有怪物生命提升X%，攻击提升X%，防御提升X%"],
            26:["支援", "当周围一圈的怪物受到攻击时将上前支援，并组成小队战斗。"],
            27:["捕捉", "当走到怪物周围十字时会强制进行战斗。"]
        }
        if type(mon_ability) is list:
            for item in mon_ability:
                check_result[ability_dict[item][0]] = ability_dict[item][1]
        elif mon_ability != 0:
            check_result[ability_dict[mon_ability][0]] = ability_dict[mon_ability][1]
        return check_result
