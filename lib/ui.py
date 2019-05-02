from lib import global_var
import pygame
from lib import ground
from sysconf import *
from project.function import draw_status_bar, get_current_enemy
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


class Menu(UIComponent):
    def __init__(self, **kwargs):
        UIComponent.__init__(self, **kwargs)
        self.index = 0

    # draw_enemy_book 绘制怪物手册
    # TODO： 绘制动态的怪物——把sprite添加到对应位置即可 和map是一样的 在发生改变时用类似draw_map的方式更新sprite
    def draw_enemy_book(self, current_index=0, map_index=None):
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
        # pygame.display.update()
        # print(f"BOOK SHOW! Index = {current_index}")

    # 注册到action_control的函数
    def action(self, event):
        key = event.key
        key_map = {pygame.K_LEFT: -6,
                   pygame.K_RIGHT: +6,
                   pygame.K_UP: -1,
                   pygame.K_DOWN: +1,
                   pygame.K_x: 'open',
                   pygame.K_ESCAPE: 'close'}
        if key in key_map:
            idx = key_map[key]
            if idx == 'open':
                if self.active:
                    self.close()
                else:
                    self.open()
                idx = 0
            elif idx == 'close':
                self.close()
                idx = 0
            if self.active:
                self.index += idx
            if self.active:
                return True
        return False
        # if self.active:
        #    self.draw_enemy_book(self.index)

    def flush(self, screen=None):
        if self.active:
            self.draw_enemy_book(self.index)
        super().flush(screen)
