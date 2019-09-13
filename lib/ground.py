from pygame import Surface
import pygame
from pygame.transform import scale
from pygame.sprite import Group
from sprite import EventSprite
from sysconf import *
from lib.utools import *
from lib import global_var

"""
    ground 概念说明：
    1. 画布：属于surface功能，相当于一个画板
    2. 可重定位：提供给父画布坐标转换的功能
    3. 树形结构：ground之间为树形关系，游戏全屏幕screen为根ground
    4. 访问协议：子ground从规则上不能操作父ground的属性，可以访问父的操作
    5. 坐标转换：为子类提供逻辑坐标到绝对坐标的转换，逻辑坐标系统需要自己继承了写
    6. 精灵显示：每个ground的内部存在一个SpriteGroup，根据层级在draw的时候顺序更新

    类比： 一个多层多房间的操场？

    需要改进：同级碰撞检测 并自适应调整、

"""

from os import path
import copy
from sprite import EventSprite

from pygame import Rect

#  基本绘制区域
#  x, y（画布左上角位置）, w, h（画布宽高）, scale（放大率）
#  如果需要逻辑坐标 继承该类 实现trans_locate函数（逻辑转物理）
#  mode（模式） = auto, copy, custom
"""
*auto 自动生成屏幕画布
*copy 传入Surface或者 GroundSurface 复制其rect
*custom 传入w,h 或 x,y,w,h 或 x,y,w,h,scale
"""


class GroundSurface:
    def __init__(self, **kwargs):
        scale = 1.0
        if "mode" in kwargs:
            mode = kwargs["mode"]
            if mode == "auto":
                surface = Surface((WIDTH, HEIGHT))  # pygame.display.set_mode((WIDTH, HEIGHT))
                self.rect = surface.get_rect()
            elif mode == "copy":
                surface = kwargs["surface"]
                if type(surface) is GroundSurface:
                    surface = surface.surface
                self.rect = surface.get_rect()
            elif mode == "custom":
                if "x" not in kwargs:
                    kwargs["x"] = 0
                if "y" not in kwargs:
                    kwargs["y"] = 0
                surface = Surface((int(kwargs["w"]), int(kwargs["h"])))
                rect = surface.get_rect()
                rect.left = kwargs["x"]
                rect.top = kwargs["y"]
                if "scale" in kwargs:
                    scale = kwargs["scale"]
                self.rect = rect
            else: # default：
                surface = Surface((WIDTH, HEIGHT))
                print("GroundSurface错误，提供的mode不存在")
                self.rect = surface.get_rect()
        else:
            surface = Surface((WIDTH,HEIGHT))
            print("GroundSurface错误，未提供mode参数")
            self.rect = surface.get_rect()

        self.block_size = BLOCK_UNIT

        self.w = self.rect.w
        self.h = self.rect.h
        self.surface = surface
        self.scale = scale
        self.parent = None
        self.layer = 0
        self.children = []
        self.group = Group()
        # 当前画布占用情况 无记忆 不考虑缝隙等复杂情况 指定的是一个“可绘制矩形范围”
        self.curpos = {"left": 0, "top": 0,
                       "right": 0,
                       "bottom": 0,
                       "mid": 0}
        self.priority = 0
        if "priority" in kwargs:
            self.priority = kwargs["priority"]

    # 增加子画布 这类画布可以是别的独立画布 也可以给出参数创建
    def add_child(self, *args):
        if len(args) == 1:
            # 插入别的画布到自适应的左上角 这样做由于对齐问题只能插一行 并且导致自适应混乱 多行需要手动重定位curpos
            ground_surface = args[0]
            rect = ground_surface.rect
            rect.left = self.curpos['left']
            rect.top = self.curpos['top']
            self.curpos['left'] += rect.w
        elif len(args) == 2:  # 自适应画布 贴边或者定在中心 第一个指定类型 第二个指定大小
            ground_surface = self.create_adaptive_surface(*args)
        elif len(args) == 3:  # 插入别的画布到指定坐标 无视碰撞
            ground_surface = args[0]
            ground_surface.rect.left = args[1]
            ground_surface.rect.top = args[2]
        else:  # 用Ground方式创建画布
            ground_surface = GroundSurface(*args)

        ground_surface.layer = self.layer + 1
        ground_surface.parent = self
        ground_surface.scale *= self.scale
        self.children.append(ground_surface)
        self.children.sort(key=lambda it: it.priority, reverse=False)

        return ground_surface

    # 自适应矩形
    def create_adaptive_surface(self, type, value):
        if type not in self.curpos:
            print("error type of ground")
            return
        w = self.rect.w
        h = self.rect.h
        t = self.curpos["top"]
        r = self.curpos["right"]
        l = self.curpos["left"]
        b = self.curpos["bottom"]
        op = {"left": Rect(l, t, value, h - t - b),
              "top": Rect(l, t, w - l - r, value),
              "right": Rect(w - value - r, t, value, h - t - b),
              "bottom": Rect(l, h - value - b, w - l - r, value),
              "mid": Rect(max(l, int((w - value) / 2)),
                          max(r, int((h - value) / 2)),
                          min(w - l - r, value), min(h - t - b, value))
              }
        rect = op[type]
        # print(rect)
        # print(rect.w)
        # print(rect.h)
        ground_surface = GroundSurface(mode="copy", surface=Surface([rect.w, rect.h]))
        ground_surface.rect.left = rect.left
        ground_surface.rect.top = rect.top
        self.curpos[type] += value
        return ground_surface

    # 填充一个surface到画布上，以变形/重复等方式 fill_rect指定填充范围 默认全图
    def fill_surface(self, surface: Surface, mode="scale", fill_rect=None):
        rect = surface.get_rect()
        if fill_rect is None:
            fill_rect = self.rect
            rect.left = 0
            rect.top = 0
        else:
            rect.left = fill_rect.left
            rect.top = fill_rect.top

        if mode == "scale":
            # print(self.rect.w,self.rect.h)
            self.surface.blit(scale(surface, (fill_rect.w, fill_rect.h)), fill_rect)
        elif mode == "repeat":
            while rect.bottom <= fill_rect.bottom:
                while rect.right <= fill_rect.right:
                    self.surface.blit(surface, rect)
                    rect.left += rect.w
                rect.left = 0
                rect.top += rect.h

    # 填充一个sprite到画布上 这个Sprite会被添加到当前画布的精灵组
    def add_sprite(self, sprite, mode="normal", fill_rect=None):
        if fill_rect is not None:
            if mode == "scale":  # 这个对精灵基本没用 放弃吧
                sprite.image = scale(sprite.image, (fill_rect.w, fill_rect.h))
            sprite.rect.left = fill_rect.left
            sprite.rect.top = fill_rect.top
        self.group.add(sprite)

    #  重定位 - 画布的内部逻辑坐标转换为外部坐标（父类可视坐标系）
    def relocate(self, *args):
        x, y = self.trans_locate(*args)
        x += self.rect.left
        y += self.rect.top
        return x, y

    #  重新设置surface大小 其他设置不变（如果增大会向右下扩张）
    def resize(self, w, h):
        self.surface = Surface((w, h))
        self.rect.w = w
        self.rect.h = h

    # 需要被实现 逻辑坐标到物理坐标的转换:
    def trans_locate(self, *args):
        """
        逻辑转物理，默认为top left
        :param args:
        :arg[3]: "up":top centerx "down": bottom centerx

        exmaple 1: map.trans_locate(12,12,'down') # 获取坐标 然后在该位置绘制敌人
        example 2: event.move(map.trans_locate(12,12,'down')) # 移动事件到12，12位置

        :return:
        """
        x, y = args[0], args[1]
        if len(args) > 2:
            if args[2] == "up":
                return int((x + 0.5) * self.block_size), y * self.block_size
            elif args[2] == "down":
                return int((x + 0.5) * self.block_size), (y + 1) * self.block_size

        return x * self.block_size, y * self.block_size

    #  刷新函数： 可以根据变化层级刷新部分内容而不是全部一起刷新
    #  !不同画布不能有不同的刷新率，刷新率以最快为准，控制动画频率在sprite的update中自行控制
    def flush(self, screen=None):
        self.group.update(pygame.time.get_ticks())
        self.group.draw(self.surface)
        self.children.sort(key=lambda it: it.priority)
        # tempSurface = Surface()
        for c in self.children:
            c.flush(screen=self.surface)
        if screen is not None:
            screen.blit(self.surface.convert_alpha(self.surface), self.rect)


    # 填充纯色（debug使用）
    def fill(self, arg):
        self.surface.fill(arg)

    # draw_text 在画布上绘制文字
    # 接受GroundSurface（画板），text（需要显示的文字），size（文字大小），color（文字颜色），x，y（xy相对坐标）
    # mode（模式，默认为画布相对方格坐标，如果mode="px"那么将为画布相对像素坐标）
    def draw_text(self, text, size, color, x, y, mode=None):
        font_name = global_var.get_value("font_name")
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if mode == "px":
            text_rect.left = x
            text_rect.top = y
        else:
            text_rect.left = x * BLOCK_UNIT
            text_rect.top = y * BLOCK_UNIT
        self.surface.blit(text_surface, text_rect)

    # draw_lines 在画布上绘制（一条或多条）线段
    # 接受points（端点数组，格式[(x, y)]），width（线条宽度），color（线条颜色）
    # mode（模式，默认为画布相对方格坐标，如果mode="px"那么将为画布相对像素坐标）
    # 例子：draw_lines([(1,1),(1,100),(100,1),(1,1)], 5, WHITE) -> 一个线条宽度为5px的白色三角形
    def draw_lines(self, points, width, color, mode=None):
        if mode == "px":
            pygame.draw.lines(self.surface, color, False, points, width)
        else:
            block_points = []
            for item in points:
                block_points.append([item[0] * BLOCK_UNIT, item[1] * BLOCK_UNIT])
            pygame.draw.lines(self.surface, color, False, block_points, width)

    # draw_rect 在画布上绘制矩形
    # start_pos（矩形左上角的坐标），格式[(x, y)]），end_pos（矩形右下角的坐标）
    # width（线条宽度），color（线条颜色）
    # mode（模式，默认为画布相对方格坐标，如果mode="px"那么将为画布相对像素坐标）
    def draw_rect(self, start_pos, end_pos, width, color, mode=None):
        if mode == "px":
            Rect = (start_pos[0], start_pos[1], end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
        else:
            Rect = (start_pos[0] * BLOCK_UNIT, start_pos[1] * BLOCK_UNIT, end_pos[0] * BLOCK_UNIT - start_pos[0] * BLOCK_UNIT, end_pos[1] * BLOCK_UNIT - start_pos[1] * BLOCK_UNIT)
        pygame.draw.rect(self.surface, color, Rect, width)
    
    # TODO: draw_icon （准备提供一个可以调用Sprite的接口）
    def draw_icon(self, map_element, x, y):
        px, py = self.trans_locate(0, 0)
        rect = Rect(px, py, self.block_size, self.block_size)
        # sprite的显示需要接通group
        name = str(map_element)
        ret = get_resource(name)
        px, py = self.trans_locate(x, y, "down")
        rect.centerx = px
        rect.bottom = py
        if type(ret) is tuple:  # 属于精灵 (注意：此时不能直接导入精灵，因为先有map后有精灵）
            img = ret[0]
            img_rect = ret[1]  # 以资源本体大小显示 用以支持超过32*32的图像
            img_rect.topleft = rect.topleft
            sp = list(ret[2])
            self.add_sprite(EventSprite(name, img, sp), fill_rect=img_rect)
        elif ret is not None:
            self.fill_surface(ret, fill_rect=rect)
