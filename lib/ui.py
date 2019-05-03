from lib import global_var
import pygame
from lib import ground
from sysconf import *
from project.function import draw_status_bar, get_current_enemy, sort_item
from project.floors import MAP_DATABASE
import math

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
        self.index = 0
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
            if idx == 'open':
                if self.active:
                    self.close()
                elif not self.PlayerCon.lock:
                    self.open()
                idx = 0
            elif idx == 'close':
                self.close()
                idx = 0
            else:
                idx = 0
            if self.active:
                self.index += idx
            if self.active:
                return True
        return False
        # if self.active:
        #    self.draw(self.index)
    
    # 刷新显示
    def flush(self, screen=None):
        if self.active:
            self.draw(self.index)
        super().flush(screen)

# 怪物手册，通过继承Menu得到
class Book(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
    
    # 绘制怪物手册
    # TODO： 绘制动态的怪物——把sprite添加到对应位置即可 和map是一样的 在发生改变时用类似draw_map的方式更新sprite
    def draw(self, current_index=0, map_index=None):
        if map_index is None:
            map_index = self.PlayerCon.floor
        # UI背景和左侧状态栏
        self.fill(SKYBLUE)
        draw_status_bar(self)
        # 获得当前地图中全部的怪物的信息
        enemy_info_list = get_current_enemy(MAP_DATABASE[map_index])
        # 如果当前楼层没有怪物
        if len(enemy_info_list) == 0:
            self.draw_text("本层无怪物", 72, BLACK, (17 * BLOCK_UNIT / 2) - (72 * 1.5), (13 * BLOCK_UNIT / 2) - 36, "px")
            global_var.set_value("index", current_index)
            return
        current_index = max(0, current_index)
        current_index = min(current_index, len(enemy_info_list) - 1)
        global_var.set_value("index", current_index)
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
# TODO: 目前并没有对index进行判断，因为还没有实现读档功能
#       目前UI极其简陋，需要进行美化
class StartMenu(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.key_map = {pygame.K_UP: -1,
                        pygame.K_DOWN: +1,
                        pygame.K_RETURN: 'close'}

    def action(self, event):
        if self.active:
            return Menu.action(self, event)
        else:
            return False

    def draw(self, current_index=0):
        # 设置index全局变量，是因为以后复写action函数的时候可以判断选中的项目
        global_var.set_value("index", current_index)
        # 此处人为指定index上下限，因为已知仅有两个选项
        current_index = max(0, current_index)
        current_index = min(1, current_index)
        self.fill(SKYBLUE)
        self.draw_text(TOWER_NAME, 64, WHITE, 6, 0)
        self.draw_text("开始游戏", 36, WHITE, 7, 6)
        self.draw_text("读取存档", 36, WHITE, 7, 7)
        if current_index == 0:
            self.draw_text("=>", 36, WHITE, 6, 6)
        if current_index == 1:
            self.draw_text("=>", 36, WHITE, 6, 7)


# 背包，通过继承Menu得到
class Backpack(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
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
                               pygame.K_ESCAPE: 'close'}

        # 通过simple和detail区分场景
        self.mode = "simple"
        self.detail_index = 0
        self.cls_index = []
    
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
        # 当前选中类别
        self.draw_text(">", 36, BLACK, 0, current_index * (BLOCK_UNIT + 50) + 30, "px")
        # 分割线
        self.draw_lines([(4,0),(4,13)], 5, BLACK)
        self.draw_lines([(4,3),(17,3)], 5, BLACK)
        # 获取分类后的背包（获得字典）
        sort_info = sort_item(category)
        # 生成物品类型数组
        if self.cls_index == []:
            for cls in sort_info:
                self.cls_index.append(cls)
        # 找出当前选中的类型
        current_cls = self.cls_index[current_index]
        current_sort_info = sort_info[current_cls]
        if current_sort_info == {}:
            self.draw_text("你没有该分类下的物品", 36, BLACK, 4, 3)
        else:
            # 生成当前类型下的物品数组
            current_sort_list = []
            for item in current_sort_info:
                current_sort_list.append(item)
            # 检测index是否超出范围
            self.detail_index = max(0, self.detail_index)
            self.detail_index = min(self.detail_index, len(current_sort_list) - 1)
            # 计算分页并从current_sort_list中提取需要展示的数据
            item_per_page = 8
            total_page = math.ceil(len(current_sort_list) / item_per_page)
            current_page = math.ceil((self.detail_index + 1) / item_per_page)
            slice_start = (current_page - 1) * item_per_page
            slice_end = min(slice_start + item_per_page, len(current_sort_list))
            current_sort_list = current_sort_list[slice_start:slice_end]
            # 绘制物品条目
            i = 0
            for item in current_sort_list:
                self.draw_text(str(current_sort_info[item]["item_name"]), 36, BLACK, 4, 3 + i)
                self.draw_text("数量：" + str(current_sort_info[item]["item_amount"]), 36, BLACK, 7, 3 + i)
                i += 1
            if self.mode == "simple":
                self.draw_rect((4, 3), (17, 4), 3, RED)
                self.draw_text("描述：" + current_sort_info[current_sort_list[0]]["item_text"], 36, BLACK, 4, 0)
            elif self.mode == "detail":
                k = self.detail_index % item_per_page
                self.draw_rect((4, 3 + k), (17, 4 + k), 3, RED)
                self.draw_text("描述：" + current_sort_info[current_sort_list[k]]["item_text"], 36, BLACK, 4, 0)
        
    # 注册到action_control的函数
    def action(self, event):
        if self.mode == "simple":
            key_map = self.key_map
            key = event.key
            if key in key_map:
                idx = key_map[key]
                if idx == 'open':
                    if self.active:
                        self.close()
                    elif not self.PlayerCon.lock:
                        self.open()
                    idx = 0
                if self.active:
                    if idx == "enter":
                        self.mode = "detail"
                        idx = 0
                    elif idx == 'close':
                        self.close()
                        idx = 0
                if self.active:
                    self.index += idx
                    return True
            return False
        if self.mode == "detail":
            key_map = self.key_map_detail
            key = event.key
            if key in key_map:
                idx = key_map[key]
                if idx == 'close':
                    self.mode = "simple"
                    self.detail_index = 0
                    idx = 0
                if self.active:
                    self.detail_index += idx
                    return True
            return False
    
    # 刷新显示
    def flush(self, screen=None):
        if self.active:
            self.draw(self.index)
        super().flush(screen)
        
