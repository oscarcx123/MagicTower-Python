# 精灵基类 用来做基本显示/逻辑物理转换的模块

import pygame

from sysconf import BLOCK_UNIT

# 逻辑坐标到物理坐标的转换 默认为RM的方式
temp_scale = BLOCK_UNIT
temp_freq = 4  # 行动一格需要的帧数 scale的倍数最好 不是也行


def temp_trans(pos):  # 仿RM 临时游戏坐标到绝对坐标转换 代表的是 centerx, bottom
    return [int((pos[0] + 0.5) * temp_scale), (pos[1] + 1) * temp_scale]


def rect_trans(rect):  # 获取rect的当前物理坐标
    return [rect.centerx, rect.bottom]


# 角色精灵类 用于动态的角色或者事件
class ActorSprite(pygame.sprite.Sprite):
    def __init__(self, id, image, pos, size, *groups):
        # id : actor id  image:surface pos(逻辑xy) size(图像个数,[行数,列数])
        super().__init__(*groups)
        self.id = id
        self.src = image
        self.pos = pos
        self.size = size
        self.face = [0, 0]  # 当前的图像（行号，列号）

        self._dx = int(image.get_width() / size[0])  # 宽度
        self._dy = int(image.get_height() / size[1])  # 高度
        self.image = self.src.subsurface(self.face[1] * self._dx, self.face[0] * self._dy, self._dx, self._dy)
        self.rect = self.image.get_rect()
        self.rect.centerx,self.rect.bottom = temp_trans(pos)

        self.moving = False
        self._walk = 0

    def update(self):  # TODO：坐标系
        self.image = self.src.subsurface(self.face[1] * self._dx, self.face[0] * self._dy, self._dx, self._dy)
        # self.rect = self.image.get_rect()
        dst_pos = temp_trans(self.pos)  # 目标的物理坐标
        cur_pos = rect_trans(self.rect)

        step = int(temp_scale / temp_freq) + int(((temp_scale % temp_freq) * 2 - 1) / temp_freq)

        def shiftleg():  # 对齐变腿
            self.face[1] = (self.face[1] + 1) % self.size[1]
            # print("换腿", self.face[1])
        def attention():
            if self.face[1] % 2 == 0:
                return
            else:
                shiftleg()

        # 步长算法： 如果有余数且余数大于步长的一半 分配到每一步上 否则之后对齐
        # 在一条轴上的移动 callback是进入对齐线前后的回调函数
        def move_axis(cur, dst, step, block, callback=None):
            """
            :param cur: 当前坐标
            :param dst: 目标坐标
            :param step: 步长
            :param block: 块长
            :param callback: 每次对齐后的函数
            :return: 当前步长
            """
            res = abs(cur - dst) % block  # 块内剩余距离
            if cur < dst:
                diff = step
            elif cur > dst:
                diff = -step
            else:
                return 0

            if 0 < res < 2*step:
                # 即将走入的区间
                if callback is not None:
                    callback()

            ldff = abs(res - abs(diff))
            if ldff < step:  # 走入对齐区
                if diff < 0:
                    diff = -res
                else:
                    diff = res
            return diff

        sx = move_axis(cur_pos[0], dst_pos[0], step, temp_scale) #, shiftleg)
        sy = move_axis(cur_pos[1], dst_pos[1], step, temp_scale) # , shiftleg)

        if self.moving:
            self._walk += 1
            if not self._walk < int(temp_freq / 2):
                self._walk = 0
                shiftleg()

        if sx != 0 or sy != 0:
            if not self.moving:
                self.moving = True
            self.rect.move_ip(sx, sy)
        elif self.moving:  # 停止立正：
            # print("立正")
            attention()
            self.moving = False

    def move(self, dir):  # TODO:渐变 | 边界判断
        if self.moving:
            return
        if dir < self.size[0]:
            self.face[0] = dir
        if dir == 0:
            self.pos[1] += 1
        if dir == 1:
            self.pos[0] -= 1
        if dir == 2:
            self.pos[0] += 1
        if dir == 3:
            self.pos[1] -= 1
        print(self.pos)
        # self.update()
