from lib import global_var
import pygame
from lib import ground
from sysconf import *
from project.function import draw_status_bar, get_current_enemy, sort_item, remove_item
from project.items import *
from project import block
import math
import os
import json

# TODO: 所有UI继承自UI组件 UI组件是集通用显示与操作响应的接口类
# UI首先是一个ground，然后具有action（需要手动注册到action_control TODO:自动注册
class UIComponent(ground.GroundSurface):
    def __init__(self, **kwargs):
        ground.GroundSurface.__init__(self, **kwargs)
        self.active = False
        self.PlayerCon = global_var.get_value("PlayerCon")

    def open(self):
        self.active = True
        self.PlayerCon.lock = True

    def close(self):
        self.active = False
        self.PlayerCon.lock = False

    def action(self):# 需要实现
        pass

# Menu （菜单）
# 菜单类提供基础的多页操作
# Menu类已经提供默认的key_map，action，flush，继承后需要编写draw函数
class Menu(UIComponent):
    def __init__(self, **kwargs):
        UIComponent.__init__(self, **kwargs)
        self.name = "菜单"
        self.current_index = 0
        self.key_map = {pygame.K_LEFT: -6,
                        pygame.K_RIGHT: +6,
                        pygame.K_UP: -1,
                        pygame.K_DOWN: +1,
                        pygame.K_x: 'open',
                        pygame.K_ESCAPE: 'close'}
    
    # 注册到action_control的函数
    def action(self, event):
        key_map = self.key_map
        key = event.key
        if key in key_map:
            idx = key_map[key]
            if self.active:
                print(self.name,key,key_map)
                if idx == 'open':
                    self.close()
                    self.group.empty()
                    idx = 0
                elif idx == 'close':
                    self.close()
                    self.group.empty()
                    idx = 0
                elif type(idx) is not int:
                    idx = 0
                if self.active:
                    self.current_index += idx
                return True
            else:
                if idx == 'open':
                    print(self.name,key,key_map)
                    if not self.PlayerCon.lock:
                        self.open()
                    idx = 0
        return False
        # if self.active:
        #    self.draw(self.current_index)
    
    # 刷新显示
    def flush(self, screen=None):
        if self.active:
            self.draw(self.current_index)
        super().flush(screen)

# 怪物手册，通过继承Menu得到
class Book(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.name = "怪物手册"
    
    # 绘制怪物手册
    # TODO： 绘制动态的怪物——把sprite添加到对应位置即可 和map是一样的 在发生改变时用类似draw_map的方式更新sprite
    def draw(self, current_index=0, map_index=None):
        if map_index is None:
            map_index = self.PlayerCon.floor
        # UI背景和左侧状态栏
        self.fill(SKYBLUE)
        draw_status_bar(self)
        # 获得当前地图中全部的怪物的信息
        CurrentMap = global_var.get_value("CurrentMap")
        enemy_info_list = get_current_enemy(CurrentMap.get_map(self.PlayerCon.floor))
        # 如果当前楼层没有怪物
        if len(enemy_info_list) == 0:
            self.draw_text("本层无怪物", 72, BLACK, (17 * BLOCK_UNIT / 2) - (72 * 1.5), (13 * BLOCK_UNIT / 2) - 36, "px")
            return
        self.current_index = max(0, self.current_index)
        self.current_index = min(self.current_index, len(enemy_info_list) - 1)
        # 计算分页并从enemy_info_list中提取需要展示的数据
        item_per_page = 6
        total_page = math.ceil(len(enemy_info_list) / item_per_page)
        current_page = math.ceil((current_index + 1) / item_per_page)
        slice_start = (current_page - 1) * item_per_page
        slice_end = min(slice_start + item_per_page, len(enemy_info_list))
        enemy_info_list = enemy_info_list[slice_start:slice_end]
        # 绘制怪物手册条目
        i = 0
        for enemy in enemy_info_list:
            self.draw_icon(enemy["mon_num_id"], 4, 2 * i)

            self.draw_text(str(enemy["mon_name"]), 30, BLACK, 6 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10, "px")
            self.draw_text("生命 " + str(enemy["mon_hp"]), 30, BLACK, 8 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10, "px")
            self.draw_text("攻击 " + str(enemy["mon_atk"]), 30, BLACK, 11 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10, "px")
            self.draw_text("防御 " + str(enemy["mon_def"]), 30, BLACK, 14 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10, "px")
            self.draw_text("金币 " + str(enemy["mon_gold"]), 30, BLACK, 8 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 46, "px")
            self.draw_text("经验 " + str(enemy["mon_exp"]), 30, BLACK, 11 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 46, "px")
            self.draw_text("伤害 " + str(enemy["damage"]), 30, BLACK, 14 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 46, "px")
            self.draw_text("临界 " + str(enemy["next_critical"]), 30, BLACK, 8 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 82, "px")
            self.draw_text("减伤 " + str(enemy["next_critical_decrease"]), 30, BLACK, 11 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 82, "px")
            self.draw_text("1防 " + str(enemy["next_def_critical"]), 30, BLACK, 14 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 82, "px")
            i += 1
        # 根据当前current_index绘制高亮框
        i = current_index % item_per_page
        self.draw_rect((4 * BLOCK_UNIT, 2 * BLOCK_UNIT * i), (17 * BLOCK_UNIT - 10, 2 * BLOCK_UNIT * (i + 1)), 3, RED,"px")


# 开始菜单，通过继承Menu得到
class StartMenu(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.name = "开始菜单"
        self.key_map = {pygame.K_UP: -1,
                        pygame.K_DOWN: +1,
                        pygame.K_RETURN: 'enter',}

    def action(self, event):
        key_map = self.key_map
        key = event.key
        if key in key_map:
            idx = key_map[key]
            if self.active:
                print(self.name,key,key_map)
                if idx == 'enter':
                    if self.current_index == 0:
                        self.close()
                        idx = 0
                    elif self.current_index == 1:
                        self.close()
                        idx = 0
                        load = global_var.get_value("LOAD")
                        load.open()
                elif type(idx) is not int:
                    idx = 0
                if self.active:
                    self.current_index += idx
                return True

    def draw(self, current_index=0):
        # 此处人为指定index上下限，因为已知仅有两个选项

        self.current_index = max(0, self.current_index)
        self.current_index = min(1, self.current_index)
        self.fill(SKYBLUE)
        self.draw_text(TOWER_NAME, 64, WHITE, 6, 0)
        self.draw_text("开始游戏", 36, WHITE, 7, 6)
        self.draw_text("读取存档", 36, WHITE, 7, 7)
        #print("Currentindex", self.active)
        if current_index == 0:
            self.draw_text("=>", 36, WHITE, 6, 6)
        if current_index == 1:
            self.draw_text("=>", 36, WHITE, 6, 7)


# 背包，通过继承Menu得到
class Backpack(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.name = "背包"
        self.key_map = {pygame.K_UP: -1,
                        pygame.K_DOWN: +1,
                        pygame.K_t: 'open',
                        pygame.K_ESCAPE: 'close',
                        pygame.K_RETURN: 'enter',
                        }
                        
        self.key_map_detail = {pygame.K_LEFT: -8,
                               pygame.K_RIGHT: +8,
                               pygame.K_UP: -1,
                               pygame.K_DOWN: +1,
                               pygame.K_RETURN: 'enter',
                               pygame.K_ESCAPE: 'close'}

        # 通过simple和detail区分场景
        self.mode = "simple"
        # 每页道具数量
        self.item_per_page = 8
        self.detail_index = 0
        self.cls_index = []
        self.current_sort_list = []
    
    # 绘制背包
    def draw(self, current_index=0):
        # UI背景和左侧类别
        self.fill(SKYBLUE)
        i = 0
        category = {"keys":"钥匙",
                     "items":"道具",
                     "constants":"永久物品",
                     "tools":"工具",
                     "equipments":"装备"}
        for item in category:
            self.draw_text(str(category[item]), 36, BLACK, BLOCK_UNIT, i * (BLOCK_UNIT + 50) + 30, "px")
            self.draw_rect((BLOCK_UNIT * 0.5, i * (BLOCK_UNIT + 50) + 30 - 10), (3.5 * BLOCK_UNIT, i * (BLOCK_UNIT + 50) + 30 - 10 + BLOCK_UNIT), 8, RED, "px")
            i += 1
        # 分割线
        self.draw_lines([(4,0),(4,13)], 5, BLACK)
        self.draw_lines([(4,3),(17,3)], 5, BLACK)
        # 获取分类后的背包（获得字典）
        sort_info = sort_item(category)
        # 生成物品类型数组
        if self.cls_index == []:
            for cls in sort_info:
                self.cls_index.append(cls)
        # 定义current_index的最大值和最小值
        self.current_index = max(0, self.current_index)
        self.current_index = min(self.current_index, len(category) - 1)
        # 当前选中类别
        self.draw_text(">", 36, BLACK, 0, self.current_index * (BLOCK_UNIT + 50) + 30, "px")
        # 找出当前选中的类型
        current_cls = self.cls_index[self.current_index]
        current_sort_info = sort_info[current_cls]
        if current_sort_info == {}:
            self.draw_text("你没有该分类下的物品", 36, BLACK, 4, 3)
        else:
            # 生成当前类型下的物品数组
            self.current_sort_list = []
            for item in current_sort_info:
                self.current_sort_list.append(item)
            # 检测index是否超出范围
            self.detail_index = max(0, self.detail_index)
            self.detail_index = min(self.detail_index, len(self.current_sort_list) - 1)
            # 计算分页并从self.current_sort_list中提取需要展示的数据
            total_page = math.ceil(len(self.current_sort_list) / self.item_per_page)
            current_page = math.ceil((self.detail_index + 1) / self.item_per_page)
            slice_start = (current_page - 1) * self.item_per_page
            slice_end = min(slice_start + self.item_per_page, len(self.current_sort_list))
            self.current_sort_list = self.current_sort_list[slice_start:slice_end]
            # 绘制物品条目
            i = 0
            for item in self.current_sort_list:
                self.draw_text(str(current_sort_info[item]["item_name"]), 36, BLACK, 4, 3 + i)
                self.draw_text("数量：" + str(current_sort_info[item]["item_amount"]), 36, BLACK, 7, 3 + i)
                i += 1
            if self.mode == "simple":
                self.draw_rect((4, 3), (17, 4), 3, RED)
                self.draw_text("描述：" + current_sort_info[self.current_sort_list[0]]["item_text"], 36, BLACK, 4, 0)
            elif self.mode == "detail":
                k = self.detail_index % self.item_per_page
                self.draw_rect((4, 3 + k), (17, 4 + k), 3, RED)
                self.draw_text("描述：" + current_sort_info[self.current_sort_list[k]]["item_text"], 36, BLACK, 4, 0)
        
    # 注册到action_control的函数
    def action(self, event):
        if self.mode == "simple":
            key_map = self.key_map
            key = event.key
            if key in key_map:
                idx = key_map[key]
                if self.active:
                    print(self.name,key,key_map)
                    if idx == 'open':
                        self.close()
                        idx = 0
                    if idx == "enter":
                        self.mode = "detail"
                        idx = 0
                    elif idx == 'close':
                        self.close()
                        idx = 0
                    self.current_index += idx
                    return True
                else:
                    if idx == 'open':
                        print(self.name,key,key_map)
                        if not self.PlayerCon.lock:
                            self.open()
                        idx = 0
            return False
        if self.mode == "detail":
            key_map = self.key_map_detail
            key = event.key
            if key in key_map:
                idx = key_map[key]
                print(self.name,key,key_map)
                if idx == "enter":
                    self.mode = "simple"
                    self.close()
                    idx = 0
                    use_result = self.use_item()
                    if use_result:
                        print("[DEBUG]道具使用成功！")
                    else:
                        print("[DEBUG]该道具不可被使用！")
                if idx == 'close':
                    self.mode = "simple"
                    self.detail_index = 0
                    idx = 0
                if self.active:
                    self.detail_index += idx
                    return True
            return False

    def use_item(self):
        k = self.detail_index % self.item_per_page
        item = self.current_sort_list[k]
        try:
            item_name_id = block.BlockData[str(item)]["id"]
            item_function = ITEMS_DATA["useItemEffect"][item_name_id]
        except KeyError:
            return False
        command = (
                f"item_result = {item_function}\n"
                f"if item_result['result'] == True:\n"
                f"    remove_item(item, 1)\n"
                f"else:\n"
                f"    print(item_result['msg'])\n"
            )
        exec(command)
        CurrentMap = global_var.get_value("CurrentMap")
        CurrentMap.set_map(self.PlayerCon.floor)
        draw_status_bar()
        return True


# 存读档菜单，通过继承Menu得到
class SaveLoadMenu(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        # 启动菜单的按键写在继承SaveLoadMenu的类中
        # 写法为：self.key_map[pygame.K_s] = 'open'
        self.key_map = {pygame.K_UP: -1,
                        pygame.K_DOWN: +1,
                        pygame.K_LEFT: -4,
                        pygame.K_RIGHT: +4,
                        pygame.K_ESCAPE: 'close',
                        pygame.K_RETURN: 'enter',}
        self.save_path = os.path.join(os.getcwd(), "save")

    def action(self, event):
        key_map = self.key_map
        key = event.key
        if key in key_map:
            idx = key_map[key]
            if self.active:
                print(self.name,key,key_map)
                if idx == 'open':
                    self.close()
                    idx = 0
                elif idx == 'close':
                    self.close()
                    idx = 0
                elif idx == 'enter':
                    # self.function为进行存读档（文件读写）的函数
                    save_status = self.function(self.current_index)
                    if save_status:
                        self.close()
                        idx = 0
                    else:
                        print("存读档错误！")
                elif type(idx) is not int:
                    idx = 0
                else:
                    self.current_index += idx
                return True
            else:
                if idx == 'open':
                    print(self.name,key,key_map)
                    if not self.PlayerCon.lock:
                        self.open()
                    idx = 0
        return False

    def draw(self, current_index=0):
        self.current_index = max(0, self.current_index)
        self.current_index = min(self.current_index, SAVE_MAX_AMOUNT - 1)
        # 计算分页并提取需要展示的数据
        item_per_page = 4
        total_page = math.ceil(SAVE_MAX_AMOUNT / item_per_page)
        current_page = math.ceil((self.current_index + 1) / item_per_page)
        slice_start = (current_page - 1) * item_per_page
        slice_end = min(slice_start + item_per_page - 1, SAVE_MAX_AMOUNT)

        # 让存档index跟实际非0自然数对应
        slice_start += 1
        slice_end += 1
        
        check_result = self.check_save_file(slice_start, slice_end)

        self.fill(SKYBLUE)
        
        # 绘制存档条目
        i = 0
        for item in check_result:
            save_number = (current_page - 1) * item_per_page + i + 1
            self.draw_text("#" + str(save_number), 30, BLACK, 4 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10, "px")
            if check_result[item]["file_exist"]:
                self.draw_text("存在存档！！", 30, BLACK, 6 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10, "px")
            else:
                self.draw_text("不存在存档！！", 30, BLACK, 6 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10, "px")
            i += 1
        # 根据当前current_index绘制高亮框
        i = current_index % item_per_page
        self.draw_rect((4 * BLOCK_UNIT, 2 * BLOCK_UNIT * i), (17 * BLOCK_UNIT - 10, 2 * BLOCK_UNIT * (i + 1)), 3, RED,"px")

    def check_save_file(self, slice_start, slice_end):
        file_name_1 = "save_"
        file_name_2 = ".json"
        file_list = []
        check_result = {}
        for i in range(slice_start, slice_end + 1):
            file_list.append(file_name_1 + str(i) + file_name_2)
        for item in file_list:
            check_result[item] = {}
            if os.path.isfile(os.path.join(self.save_path, item)):
                check_result[item]["file_exist"] = True
            else:
                check_result[item]["file_exist"] = False
        return check_result


# 存档菜单，通过继承SaveLoadMenu得到
class SaveMenu(SaveLoadMenu):
    def __init__(self, **kwargs):
        SaveLoadMenu.__init__(self, **kwargs)
        self.name = "存档菜单"
        self.key_map[pygame.K_s] = 'open'

    def function(self, current_index):
        CurrentMap = global_var.get_value("CurrentMap")
        save_file = {}
        save_file["hero"] = {}
        save_file["hero"]["hp"] = self.PlayerCon.hp
        save_file["hero"]["attack"] = self.PlayerCon.attack
        save_file["hero"]["defend"] = self.PlayerCon.defend
        save_file["hero"]["mdefend"] = self.PlayerCon.mdefend
        save_file["hero"]["gold"] = self.PlayerCon.gold
        save_file["hero"]["exp"] = self.PlayerCon.exp
        save_file["hero"]["floor"] = self.PlayerCon.floor
        save_file["hero"]["item"] = self.PlayerCon.item
        save_file["hero"]["pos"] = self.PlayerCon.pos
        save_file["map"] = CurrentMap.MAP_DATABASE

        current_index += 1
        file_name_1 = "save_"
        file_name_2 = ".json"
        full_file_name = file_name_1 + str(current_index) + file_name_2
        full_path = os.path.join(self.save_path, full_file_name)
        with open((full_path), "w") as f:
            json.dump(save_file, f)
        print("存档成功！")
        return True


# 读档菜单，通过继承SaveLoadMenu得到
class LoadMenu(SaveLoadMenu):
    def __init__(self, **kwargs):
        SaveLoadMenu.__init__(self, **kwargs)
        self.name = "读档菜单"
        self.key_map[pygame.K_d] = 'open'

    def function(self, current_index):
        current_index += 1
        file_name_1 = "save_"
        file_name_2 = ".json"
        full_file_name = file_name_1 + str(current_index) + file_name_2
        full_path = os.path.join(self.save_path, full_file_name)
        if os.path.isfile(full_path):
            with open(full_path) as f:
                save_file = json.load(f)
            CurrentMap = global_var.get_value("CurrentMap")
            self.PlayerCon.hp = save_file["hero"]["hp"]
            self.PlayerCon.attack = save_file["hero"]["attack"]
            self.PlayerCon.defend = save_file["hero"]["defend"]
            self.PlayerCon.mdefend = save_file["hero"]["mdefend"]
            self.PlayerCon.gold = save_file["hero"]["gold"]
            self.PlayerCon.exp = save_file["hero"]["exp"]
            self.PlayerCon.floor = save_file["hero"]["floor"]
            self.PlayerCon.item = {}
            for item_num_id in save_file["hero"]["item"]:
                self.PlayerCon.item[int(item_num_id)] = save_file["hero"]["item"][item_num_id]
            self.PlayerCon.pos = save_file["hero"]["pos"]
            CurrentMap.MAP_DATABASE = save_file["map"]
            CurrentMap.set_map(self.PlayerCon.floor)
            global_var.set_value("CurrentMap", CurrentMap)
            draw_status_bar()
            self.PlayerCon.change_hero_loc(self.PlayerCon.pos[0], self.PlayerCon.pos[1])
            print("读档成功！")
            return True
        else:
            print("读取了不存在的存档!")
            return False
        