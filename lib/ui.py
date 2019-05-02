from lib import global_var
import pygame
from lib import ground


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
        from project.function import draw_enemy_book  # TODO:可能要拆过来？
        draw_enemy_book(current_index, map_index, self)

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
