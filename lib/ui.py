import math
import os
import json
import re
import pygame
from pygame import Surface
from pygame.sprite import Sprite
from pygame.transform import scale
from pygame import Rect

from lib import global_var, WriteLog
from lib import ground
from sysconf import *
from project.items import *
from project import block

# TODO: 所有UI继承自UI组件 UI组件是集通用显示与操作响应的接口类
# UI首先是一个ground，然后具有action（需要手动注册到action_control TODO:自动注册
class UIComponent(ground.GroundSurface):
    def __init__(self, **kwargs):
        ground.GroundSurface.__init__(self, **kwargs)
        self.active = False
        self.PlayerCon = global_var.get_value("PlayerCon")
        self.FUNCTION = global_var.get_value("FUNCTION")

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
                WriteLog.debug(__name__, (self.name,key,key_map))
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
                else:
                    self.current_index += idx
                    self.group.empty()
                return True
            else:
                if idx == 'open':
                    WriteLog.debug(__name__, (self.name,key,key_map))
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

# BlankPage （全屏空白页）
# 空白页类提供基础的单页展示
# Menu类已经提供默认的key_map，action，flush，继承后需要编写draw函数
class BlankPage(UIComponent):
    def __init__(self, **kwargs):
        UIComponent.__init__(self, **kwargs)
        self.name = "空白页"
        self.key_map = {pygame.K_h: 'open',
                        pygame.K_ESCAPE: 'close'}
    
    # 注册到action_control的函数
    def action(self, event):
        key_map = self.key_map
        key = event.key
        if key in key_map:
            idx = key_map[key]
            if self.active:
                WriteLog.debug(__name__, (self.name,key,key_map))
                if idx == 'open':
                    self.close()
                    idx = 0
                elif idx == 'close':
                    self.close()
                    idx = 0
                return True
            else:
                if idx == 'open':
                    WriteLog.debug(__name__, (self.name,key,key_map))
                    if not self.PlayerCon.lock:
                        self.open()
                    idx = 0
        return False
    
    # 刷新显示
    def flush(self, screen=None):
        if self.active:
            self.draw()
        super().flush(screen)

# 怪物手册，通过继承Menu得到
class Book(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.name = "怪物手册"
    
    # 绘制怪物手册
    def draw(self, current_index=0, map_index=None):
        if map_index is None:
            map_index = self.PlayerCon.floor
        # UI背景和左侧状态栏
        self.fill(SKYBLUE)
        self.FUNCTION.draw_status_bar()
        # 获得当前地图中全部的怪物的信息
        CurrentMap = global_var.get_value("CurrentMap")
        enemy_info_list = self.FUNCTION.get_current_enemy(CurrentMap.get_map(self.PlayerCon.floor))
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
        drawSprite = len(self.group.spritedict) == 0
        for enemy in enemy_info_list:
            if drawSprite : self.draw_icon(enemy["mon_num_id"], 4, 2 * i)

            self.draw_text(str(enemy["mon_name"]), 30, BLACK, 6 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10, "px")
            
            # 显示怪物特殊能力
            ability_text = self.FUNCTION.get_ability_text(enemy["mon_ability"])
            if len(ability_text) == 0:
                pass
            elif len(ability_text) == 1:
                for item in ability_text:
                    self.draw_text(item, 30, BLACK, 6 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 46, "px")
            elif len(ability_text) == 2:
                temp_index = 1
                for item in ability_text:
                    self.draw_text(item, 30, BLACK, 6 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10 + 36 * temp_index, "px")
                    temp_index += 1
            else:
                self.draw_text("能力太多", 30, BLACK, 6 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 46, "px")

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
                WriteLog.debug(__name__, (self.name,key,key_map))
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
                else:
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
        sort_info = self.FUNCTION.sort_item(category)
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
                self.draw_text("数量：" + str(current_sort_info[item]["item_amount"]), 36, BLACK, 10, 3 + i)
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
                    WriteLog.debug(__name__, (self.name,key,key_map))
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
                        WriteLog.debug(__name__, (self.name,key,key_map))
                        if not self.PlayerCon.lock:
                            self.open()
                        idx = 0
            return False
        if self.mode == "detail":
            key_map = self.key_map_detail
            key = event.key
            if key in key_map:
                idx = key_map[key]
                WriteLog.debug(__name__, (self.name,key,key_map))
                if idx == "enter":
                    self.mode = "simple"
                    self.close()
                    idx = 0
                    use_result = self.use_item()
                    if use_result:
                        WriteLog.debug(__name__, "道具使用成功！")
                    else:
                        WriteLog.debug(__name__, "该道具不可被使用！")
                    return True
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
            item_type = ITEMS_DATA["items"][item_name_id]["cls"]
            item_function = ITEMS_DATA["useItemEffect"][item_name_id]
        except KeyError:
            return False
        command = (
                f"item_result = {item_function}\n"
                f"if item_result['result'] == True:\n"
                f"    if '{item_type}' != 'constants':\n"
                f"        self.FUNCTION.remove_item(item, 1)\n"
                f"else:\n"
                f"    print(item_result['msg'])\n"
            )
        exec(command)
        CurrentMap = global_var.get_value("CurrentMap")
        CurrentMap.set_map(self.PlayerCon.floor)
        self.FUNCTION.draw_status_bar()
        return True


# 存读档菜单，通过继承Menu得到
class SaveLoadMenu(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        # 启动菜单的按键写在继承SaveLoadMenu的类中
        # 写法为：self.key_map[pygame.K_s] = 'open'
        self.key_map = {pygame.K_UP: -1,
                        pygame.K_DOWN: +1,
                        pygame.K_LEFT: -6,
                        pygame.K_RIGHT: +6,
                        pygame.K_ESCAPE: 'close',
                        pygame.K_RETURN: 'enter',}
        self.save_path = os.path.join(os.getcwd(), "save")

    def action(self, event):
        key_map = self.key_map
        key = event.key
        if key in key_map:
            idx = key_map[key]
            if self.active:
                WriteLog.debug(__name__, (self.name,key,key_map))
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
                        WriteLog.debug(__name__, "存读档错误！")
                elif type(idx) is not int:
                    idx = 0
                else:
                    self.current_index += idx
                return True
            else:
                if idx == 'open':
                    WriteLog.debug(__name__, (self.name,key,key_map))
                    if not self.PlayerCon.lock:
                        self.open()
                    idx = 0
        return False

    def draw(self, current_index=0):
        self.current_index = max(0, self.current_index)
        self.current_index = min(self.current_index, SAVE_MAX_AMOUNT - 1)
        # 计算分页并提取需要展示的数据
        item_per_page = 6
        total_page = math.ceil(SAVE_MAX_AMOUNT / item_per_page)
        current_page = math.ceil((self.current_index + 1) / item_per_page)
        slice_start = (current_page - 1) * item_per_page
        slice_end = min(slice_start + item_per_page - 1, SAVE_MAX_AMOUNT - 1)

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
            if len(check_result[item]) > 0:
                # 显示勇士基础数值（HP/ATK/DEF/MDEF）
                self.draw_text("HP " + str(check_result[item]["hp"]) + " / ATK " + str(check_result[item]["attack"]) + " / DEF " + str(check_result[item]["defend"]) + " / MDEF " + str(check_result[item]["mdefend"]), 30, BLACK, 6 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10, "px")
                # 显示勇士位置（楼层 & 坐标）
                self.draw_text(str(check_result[item]["floor"]) + "F @ " + str((check_result[item]["pos"][0], check_result[item]["pos"][1])), 30, BLACK, 6 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 46, "px")
                # 显示存档时间（格式YYYY-MM-DD HH:MM:SS）
                self.draw_text(str(check_result[item]["time"]), 30, BLACK, 11 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 46, "px")
            else:
                self.draw_text("不存在存档！！", 30, BLACK, 6 * BLOCK_UNIT, (2 * i * BLOCK_UNIT) + 10, "px")
            i += 1
        # 根据当前current_index绘制高亮框
        i = current_index % item_per_page
        self.draw_rect((4 * BLOCK_UNIT, 2 * BLOCK_UNIT * i), (17 * BLOCK_UNIT - 10, 2 * BLOCK_UNIT * (i + 1)), 3, RED,"px")
        # 显示当前页数
        self.draw_text(f"{current_page} / {total_page}", 30, BLACK, 9 * BLOCK_UNIT, (12 * BLOCK_UNIT) + 10, "px")

    def check_save_file(self, slice_start, slice_end):
        file_name_1 = "save_"
        file_name_2 = ".json"
        file_list = []
        check_result = {}
        for i in range(slice_start, slice_end + 1):
            file_list.append(file_name_1 + str(i) + file_name_2)
        for item in file_list:
            check_result[item] = {}
            full_path = os.path.join(self.save_path, item)
            if os.path.isfile(full_path):
                with open(full_path) as f:
                    save_file = json.load(f)
                check_result[item]["hp"] = save_file["hero"]["hp"]
                check_result[item]["attack"] = save_file["hero"]["attack"]
                check_result[item]["defend"] = save_file["hero"]["defend"]
                check_result[item]["mdefend"] = save_file["hero"]["mdefend"]
                check_result[item]["floor"] = save_file["hero"]["floor"]
                check_result[item]["pos"] = save_file["hero"]["pos"]
                check_result[item]["time"] = save_file["time"]
        return check_result


# 存档菜单，通过继承SaveLoadMenu得到
class SaveMenu(SaveLoadMenu):
    def __init__(self, **kwargs):
        SaveLoadMenu.__init__(self, **kwargs)
        self.name = "存档菜单"
        self.key_map[pygame.K_s] = 'open'

    def function(self, current_index):
        return self.FUNCTION.save(current_index)


# 读档菜单，通过继承SaveLoadMenu得到
class LoadMenu(SaveLoadMenu):
    def __init__(self, **kwargs):
        SaveLoadMenu.__init__(self, **kwargs)
        self.name = "读档菜单"
        self.key_map[pygame.K_d] = 'open'

    def function(self, current_index):
        return self.FUNCTION.load(current_index)


# 楼层传送器，通过继承Menu得到
class Fly(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.name = "楼层传送器"
        self.key_map = {pygame.K_LEFT: -1,
                        pygame.K_RIGHT: +1,
                        pygame.K_UP: -4,
                        pygame.K_DOWN: +4,
                        pygame.K_g: 'open',
                        pygame.K_ESCAPE: 'close',
                        pygame.K_RETURN: 'enter'}
        
        CurrentMap = global_var.get_value("CurrentMap")
        self.floor_index = CurrentMap.floor_index["index"]
        self.max_floor_index = len(self.floor_index) - 1
        self.floor_per_row = 4
    
    def action(self, event):
        key_map = self.key_map
        key = event.key
        if key in key_map:
            idx = key_map[key]
            if self.active:
                WriteLog.debug(__name__, (self.name,key,key_map))
                if idx == 'enter':
                    if self.floor_index[self.current_index] in self.PlayerCon.visited:
                        self.FUNCTION.change_floor("fly", floor=self.current_index)
                        self.close()
                        idx = 0
                    else:
                        print(f"你还没去过{self.floor_index[self.current_index]}！")
                elif idx == 'open':
                    self.close()
                    idx = 0
                elif idx == 'close':
                    self.close()
                    idx = 0
                elif type(idx) is not int:
                    idx = 0
                else:
                    self.current_index += idx
                return True
            else:
                if idx == 'open':
                    WriteLog.debug(__name__, (self.name,key,key_map))
                    if not self.PlayerCon.lock:
                        if self.FUNCTION.has_item(46):
                            self.open()
                            self.current_index = self.floor_index.index(self.floor_index[self.PlayerCon.floor])
                        else:
                            print("你还没有楼层传送器！")
                    idx = 0
        return False

    # 绘制楼层传送器
    def draw(self, current_index=0):
        self.current_index = max(0, self.current_index)
        self.current_index = min(self.current_index, self.max_floor_index)
        # UI背景和左侧状态栏
        self.fill(SKYBLUE)
        self.FUNCTION.draw_status_bar()
        # 绘制楼层传送器条目
        cnt = 0
        for floor in self.floor_index:
            self.draw_floor(floor, cnt)
            cnt += 1
 
        # 根据当前current_index绘制高亮框
        temp_x = current_index % self.floor_per_row
        temp_y = current_index // self.floor_per_row
        self.draw_rect(((4 + 3 * temp_x) * BLOCK_UNIT, temp_y * BLOCK_UNIT), ((4 + 3 * (temp_x + 1)) * BLOCK_UNIT, (temp_y + 1) * BLOCK_UNIT), 3, RED,"px")

    # 绘制楼层传送器中的楼层
    def draw_floor(self, floor, cnt):
        temp_x = cnt % self.floor_per_row
        temp_y = cnt // self.floor_per_row
        if floor in self.PlayerCon.visited:
            floor_color = BLACK
        else:
            floor_color = GRAY
        self.draw_text(str(floor), 30, floor_color, (5 + 3 * temp_x) * BLOCK_UNIT, temp_y * BLOCK_UNIT + 10, "px")


# 帮助页面，通过继承BlankPage得到
class Help(BlankPage):
    def __init__(self, **kwargs):
        BlankPage.__init__(self, **kwargs)
        self.name = "楼层传送器"
        self.contents = [
            "X = 怪物手册",
            "G = 楼层传送器",
            "T = 玩家背包（带二级菜单）",
            "S = 存档界面",
            "D = 读档界面",
            "A = 撤回上一关键步（打怪&开门）",
            "Z = 勇士转身（顺时针）",
            "H = 帮助界面",
            "B = 文本框Demo（测试用）",
            "P = 开关显伤层（默认开启）",
            "ESC = 返回操作",
            "Enter = 确认操作"
        ]


    def draw(self):
        cnt = 0
        self.fill(SKYBLUE)
        self.FUNCTION.draw_status_bar()
        for text in self.contents:
            self.draw_text(text, 30, BLACK, 5 * BLOCK_UNIT, (cnt * BLOCK_UNIT), "px")
            cnt += 1


# 商店基类，通过继承Menu得到
class Shop(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.name = "商店"
        self.price = 0
        self.price_increment = 0
        self.text = ""
        self.key_map = {pygame.K_UP: -1,
                        pygame.K_DOWN: +1,
                        pygame.K_ESCAPE: 'close',
                        pygame.K_RETURN: 'enter'}
        self.choices = {}

    # 继承之后，可以通过复写，把任何需要动态更新的文字放这个函数    
    def update_text(self):
        pass

    def action(self, event):
        key_map = self.key_map
        key = event.key
        if key in key_map:
            idx = key_map[key]
            if self.active:
                WriteLog.debug(__name__, (self.name,key,key_map))
                if idx == 'enter':
                    self.purchase()
                    self.group.empty()
                    self.close()
                    idx = 0
                elif idx == 'close':
                    self.group.empty()
                    self.close()
                    idx = 0
                elif type(idx) is not int:
                    idx = 0
                else:
                    self.current_index += idx
                return True
        return False

    # 绘制商店
    def draw(self, current_index=0):
        self.current_index = max(0, self.current_index)
        self.current_index = min(self.current_index, len(self.choices) - 1)
        # 绘制商店条目
        cnt = 0
        text = ""
        text = text + self.name + "\n" + self.text + "\n"
        # 根据当前current_index绘制高亮框
        for choice in self.choices:
            if cnt == self.current_index:
                text = text + "=>" + choice + "\n"
            else:
                text = text + choice + "\n"
            cnt += 1
        # 展示选项框
        self.text_obj = TextWin("mid", content=text, TEXT_WIN_WIDTH=500, text_loc="middle")
        self.text_obj.drawText()
        self.text_obj.show_on()
        self.add_sprite(self.text_obj)
        
    # 进行对应的购买操作
    def purchase(self):
        command = list(self.choices.items())[self.current_index][1]
        if command != "self.close()":
            if self.PlayerCon.gold >= self.price:
                self.PlayerCon.gold -= self.price
                self.price += self.price_increment
                exec(command)
                self.update_text()
                self.FUNCTION.draw_status_bar()
                print("购买成功！")
            else:
                print("你不够钱！")


# 商店1，通过继承商店基类得到
class Shop1(Shop):
    def __init__(self, **kwargs):
        Shop.__init__(self, **kwargs)
        self.name = "无情的恰饼机器"
        self.price = 16
        self.update_text()
        self.choices = {
            "生命+175": "self.PlayerCon.hp += 175",
            "攻击+2": "self.PlayerCon.attack += 2",
            "防御+2": "self.PlayerCon.defend += 2",
            "离开": "self.close()",
        }

    def update_text(self):
        self.text = f"给我{self.price}月饼就可以："

# 商店2，通过继承商店基类得到
class Shop2(Shop):
    def __init__(self, **kwargs):
        Shop.__init__(self, **kwargs)
        self.name = "有爱的蹭饭星人"
        self.price = 40
        self.update_text()
        self.choices = {
            "生命+520": "self.PlayerCon.hp += 520",
            "攻击+6": "self.PlayerCon.attack += 6",
            "防御+6": "self.PlayerCon.defend += 6",
            "离开": "self.close()",
        }

    def update_text(self):
        self.text = f"给我{self.price}月饼就可以："

# 选项框，通过继承商店基类得到（都是类似的菜单）
class ChoiceBox(Shop):
    def __init__(self, **kwargs):
        Shop.__init__(self, **kwargs)
        self.name = ""
        self.choices = {}

    def init(self, text, choices):
        self.choices = {}
        self.name = text
        for item in choices:
            text = item["text"]
            action = item["action"]
            self.choices[text] = action

    def do_action(self):
        EVENTFLOW = global_var.get_value("EVENTFLOW")
        command = list(self.choices.items())[self.current_index][1]
        EVENTFLOW.insert_action(command)
        
    def action(self, event):
        key_map = self.key_map
        key = event.key
        if key in key_map:
            idx = key_map[key]
            if self.active:
                WriteLog.debug(__name__, (self.name,key,key_map))
                if idx == 'enter':
                    self.do_action()
                    self.close()
                    idx = 0
                elif type(idx) is not int:
                    idx = 0
                else:
                    self.current_index += idx
                return True
        return False

# 文本框
class TextBox(UIComponent):
    def __init__(self, **kwargs):
        UIComponent.__init__(self, **kwargs)
        self.name = "文本框"
        self.key_map = {pygame.K_RETURN: 'enter'}
    
    # 注册到action_control的函数
    def action(self, event):
        key_map = self.key_map
        key = event.key
        if key in key_map:
            idx = key_map[key]
            if self.active:
                WriteLog.debug(__name__, (self.name,key,key_map))
                if idx == 'enter':
                    status = self.next()
                    if status == False:
                        self.close()
                        idx = 0
                return True
        return False
    
    # 刷新显示
    def flush(self, screen=None):
        if self.active:
            self.draw()
        super().flush(screen)

    def show(self, text):
        if not self.PlayerCon.lock:
            self.text_obj = TextWin("mid", text)
            if len(self.text_obj.line_list) > self.text_obj.line_num:
                self.text_obj.res_content = self.text_obj.line_list[self.text_obj.line_num:]
                print("res", self.text_obj.res_content)
                self.text_obj.line_list = self.text_obj.line_list[:self.text_obj.line_num]
            self.text_obj.drawText()
            self.text_obj.show_on()
            self.add_sprite(self.text_obj)
            self.open()

    def draw(self):
        pass

    def next(self):
        if self.text_obj.res_content is None:
            status = self.text_obj.updateText()
            return status
        elif len(self.text_obj.res_content) > self.text_obj.line_num:
            self.text_obj.line_list = self.text_obj.res_content[:self.text_obj.line_num]
            self.text_obj.res_content = self.text_obj.res_content[self.text_obj.line_num:]
            print("res", self.text_obj.res_content)
            status = self.text_obj.updateText()
            return status
        elif len(self.text_obj.res_content) >= 1:
            h = len(self.text_obj.res_content) * self.text_obj.dh + 2 * self.text_obj.TEXT_TOP_BOARD
            res_content = self.text_obj.res_content
            res_content.insert(0, h)
            self.group.empty()
            self.text_obj = TextWin("mid", res_content)
            self.add_sprite(self.text_obj)
            self.text_obj.drawText()
            self.text_obj.show_on()
            
# 显伤层
class ShowDamage(UIComponent):
    def __init__(self, **kwargs):
        UIComponent.__init__(self, **kwargs)
        self.name = "显伤层"
        self.showing = False
        self.damage_cache = None
        self.key_map = {pygame.K_p: 'open'}
        self.PlayerCon = global_var.get_value("PlayerCon")
        self.CurrentMap = global_var.get_value("CurrentMap")
    
    def open(self):
        self.showing = True
        self.CurrentMap.show_damage_update = True

    def close(self):
        self.showing = False

    # 注册到action_control的函数
    def action(self, event):
        key_map = self.key_map
        key = event.key
        if key in key_map:
            idx = key_map[key]
            if self.showing:
                WriteLog.debug(__name__, (self.name,key,key_map))
                if idx == 'open':
                    self.close()
                    idx = 0
                return True
            else:
                if idx == 'open':
                    WriteLog.debug(__name__, (self.name,key,key_map))
                    if not self.PlayerCon.lock:
                        self.open()
                    idx = 0
        return False
    
    # 刷新显示
    def flush(self, screen=None):
        if self.showing:
            self.draw()
        super().flush(screen)

    def draw(self):
        a = pygame.time.get_ticks()
        content = []
        for monster in self.CurrentMap.damage_layer_cache:
            for loc in self.CurrentMap.damage_layer_cache[monster]["loc"]:
                text_obj = {}
                text_obj["x"] = (loc[0] + 4) * BLOCK_UNIT
                text_obj["y"] = loc[1] * BLOCK_UNIT + 15
                text_obj["text"] = str(self.CurrentMap.damage_layer_cache[monster]["critical"])
                text_obj2 = {}
                text_obj2["x"] = (loc[0] + 4) * BLOCK_UNIT
                text_obj2["y"] = loc[1] * BLOCK_UNIT + 40
                text_obj2["text"] = str(self.CurrentMap.damage_layer_cache[monster]["damage"])
                content.append(text_obj)
                content.append(text_obj2)
        self.draw_bulk_stroke_text(content, 24, WHITE, BLACK, "px")
        b = pygame.time.get_ticks()
        print(b - a)
        #self.draw_stroke_text(str(self.CurrentMap.damage_layer_cache[monster]["critical"]), 24, WHITE, BLACK, (loc[0] + 4) * BLOCK_UNIT, loc[1] * BLOCK_UNIT + 15, "px")
        #self.draw_stroke_text(str(self.CurrentMap.damage_layer_cache[monster]["damage"]), 24, WHITE, BLACK, (loc[0] + 4) * BLOCK_UNIT, loc[1] * BLOCK_UNIT + 40, "px")


# 窗口基类
class WinBase(Sprite):
    def __init__(self, x, y, w, h, dir=None):
        super().__init__()
        self.winSkinPath = "img/winskin.png"
        self.src = pygame.image.load(self.winSkinPath).convert_alpha()
        self.pos = [x, y]  # windows的坐标就是物理坐标 left、top
        self.show = False
        self.src_show = self.init_wind(w, h, dir)
        self.dir = dir

        self.image = self.src_show  # Surface([w, h])
        self.rect = self.image.get_rect()
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]
        #print("st", self.rect)
        self.alpha = 255

    def trans_image(self, params):  # 把原图转成设备显示的surface
        if len(params) == 3:
            # print(params)
            return scale(self.src.subsurface(params[0]), params[1]), params[2]
        else:
            return self.src.subsurface(params[0]), params[1]

    def init_wind(self, w, h, dir):
        x, y = 0, 0  # self.pos[0], self.pos[1]
        scale_list = [
            (Rect(0, 0, 128, 128), (w - 4, h - 4), Rect(x + 2, y + 2, w - 4, h - 4)),  # back
            (Rect(144, 0, 32, 16), (w - 32, 16), Rect(x + 16, y, w - 32, 16)),  # top
            (Rect(128, 16, 16, 32), (16, h - 32), Rect(x, y + 16, 16, h - 32)),  # left
            (Rect(176, 16, 16, 32), (16, h - 32), Rect(x + w - 16, y + 16, 16, h - 32)),  # right
            (Rect(144, 48, 32, 16), (w - 32, 16), Rect(x + 16, y + h - 16, w - 32, 16)),  # bottom
            (Rect(128, 0, 16, 16), Rect(x, y, 16, 16)),  # top left
            (Rect(176, 0, 16, 16), Rect(x + w - 16, y, 16, 16)),  # top right
            (Rect(128, 48, 16, 16), Rect(x, y + h - 16, 16, 16)),  # bottom left
            (Rect(176, 48, 16, 16), Rect(x + w - 16, y + h - 16, 16, 16)),  # bottom right
        ]
        src_dir = {"up": (Rect(128, 96, 32, 32), Rect(x + int(w / 2), y + h - 3, 32, 32)),
                   "down": (Rect(160, 96, 32, 32), Rect(x + int(w / 2), y - 29, 32, 32))
                   }
        if dir is not None:
            scale_list.append(src_dir[dir])

        blit_list = [self.trans_image(fmt) for fmt in scale_list]
        ret = Surface([w, h])
        for l1, l2 in blit_list:
            ret.blit(l1, l2)
        # ret.blits(blit_list)
        return ret

    def show_off(self):
        self.show = False
        # self.image = Surface([self.rect.w, self.rect.h])
        self.src_show.set_alpha(0)

    def show_on(self):
        self.show = True
        self.image = self.src_show
        self.src_show.set_alpha(self.alpha)
        # self.rect = self.image.get_rect()

    def set_alpha(self, value):
        if type(value) is float:
            self.alpha = int(255 * value)
        self.src_show.set_alpha(self.alpha)

    def flush_skin(self):  # 刷新
        self.src_show = self.init_wind(self.rect.w, self.rect.h, self.dir)
        self.image = self.src_show

    def update(self, *args):
        # 窗口变化- 坐标位置
        # print('update')
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]

# 剧情文字窗口
# loc_type = 文本框在游戏窗口的位置
# content = 显示的内容
# is_talk = 带箭头的对话框
class TextWin(WinBase):
    def __init__(self, loc_type, content=None, is_talk=False, TEXT_WIN_WIDTH=int((WIDTH - 4 * BLOCK_UNIT) - 30), text_loc="left"):
        # 正则匹配半角字符
        self.dw_pattern = re.compile("[\x00-\xff]", re.A)
        # 字体路径
        self.font_name = "resource/simhei.ttf"
        # 文本框窗口的宽度
        self.TEXT_WIN_WIDTH = TEXT_WIN_WIDTH
        # 文本的侧边距
        self.TEXT_LEFT_BOARD = 40
        # 文本的顶边距
        self.TEXT_TOP_BOARD = 34
        # 文本方位（靠左，居中，靠右）
        self.text_loc = text_loc
        self.size = 36
        self.line_num = 10
        self.font = pygame.font.Font(self.font_name, self.size)
        self.dw = self.font.render("字", True, WHITE).get_rect().w  # 全角宽
        self.dh = self.font.get_height()
        # x, y, w, h -> 窗口左上角坐标(x, y)，窗口宽w，高h
        # 计算窗口左上角坐标(x, y)，其中x坐标为居中
        self.x = int(((WIDTH + 4 * BLOCK_UNIT) - self.TEXT_WIN_WIDTH) / 2)
        self.y = 0  # 默认贴边
        self.w = self.TEXT_WIN_WIDTH
        if type(content) is list:
            self.h = content[0]
            content.pop(0)
            self.line_list = content
        else:
            self.h = self.get_win_height(content)
        self.is_talk = is_talk
        if loc_type == "mid":
            self.y = int(HEIGHT / 2 - self.h / 2)
        elif loc_type == "down":
            self.y = HEIGHT - self.h
        elif loc_type == "auto":
            pass
            # TODO： 显示在头上的对话框 & 根据坐标/字数自适应大小对话框
            # 需要建立一个界面地图坐标转换接口，并且把各个界面分离开来
        #print(self.x, self.y, self.w, self.h)
        super().__init__(self.x, self.y, self.w, self.h)
        self.content = ""
        self.res_content = None

    def get_win_height(self, content):
        line_len = int((self.w - 2 * self.TEXT_LEFT_BOARD) / self.dw)  # 行长        

        self.line_list = []

        def get_real_len(s):
            return len(s) - int(len(self.dw_pattern.findall(s)) * 0.5 + 0.6)

        def align_char(content):
            clen = 0
            line = ""
            while clen < line_len and content != '':
                tlen = line_len - clen
                #print(tlen)
                tstr = content[:tlen]
                line += tstr
                clen += get_real_len(tstr)
                content = content[tlen:]
            if content != '' and get_real_len(content) <= 2:
                line += content
            #print("对齐长度：", get_real_len(line))
            return line

        for content in content.split('\n'):
            while content != '':
                s = align_char(content)
                self.line_list.append(s)
                content = content[len(s):]
        
        if len(self.line_list) > self.line_num:
            h = self.line_num * self.dh + 2 * self.TEXT_TOP_BOARD
        else:
            h = len(self.line_list) * self.dh + 2 * self.TEXT_TOP_BOARD
        return h

    def drawText(self, size=None, content=None):
        ct = 0
        for text in self.line_list:
            text_surface = self.font.render(text, True, WHITE)
            text_rect = text_surface.get_rect()
            #print(text_rect)
            if self.text_loc == "left":
                text_rect.left = self.TEXT_LEFT_BOARD  # self.pos[0]
            elif self.text_loc == "middle":
                text_rect.left = int((self.TEXT_WIN_WIDTH - self.dw * len(text)) / 2)
            text_rect.top = self.TEXT_TOP_BOARD + ct * self.dh  # + self.pos[1]
            self.src_show.blit(text_surface, text_rect)
            ct += 1

    def updateText(self):
        #print("self.res_content", self.res_content)
        if self.res_content is not None:
            self.flush_skin()
            self.drawText()
            return True
        else:
            self.show_off()
            return False

    def update(self, *args):
        super().update(args)

