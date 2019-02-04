# 精灵基类 用来做基本显示/逻辑物理转换的模块

import pygame
from sysconf import *

# 逻辑坐标到物理坐标的转换 默认为RM的方式
temp_scale = BLOCK_UNIT
temp_freq = 4  # 行动一格需要的帧数 scale的倍数最好 不是也行


def temp_trans(pos):  # 仿RM 临时游戏坐标到绝对坐标转换 代表的是 centerx, bottom
    return [int((pos[0] + 4.5) * temp_scale), (pos[1] + 1) * temp_scale]


def rect_trans(rect):  # 获取rect的当前物理坐标
    return [rect.centerx, rect.bottom]


import threading


# 事件原型精灵 有皮的事件都能用
# 因为是原型精灵 与地图位置无关 内部坐标仅仅是rect 初始均为0,0
class EventSprite(pygame.sprite.Sprite):
    def __init__(self, id, image, shape, face=None, animate=True):
        """
        :param args:
        id image shape [face:(x,y)] [dynamic:bool]
        shape : h * w 动作类型数 * 动作帧数
        """
        super().__init__()
        self.id = id
        self.src = image
        self.shape = shape
        self.face = [0, 0]
        if face is not None:
            self.face = face
        self.animate = animate
        self.animate_speed = 250
        self.moving = False
        self._dx = int(image.get_width() / shape[1])  # 宽度
        self._dy = int(image.get_height() / shape[0])  # 高度
        self.image = self.src.subsurface(self.face[1] * self._dx, self.face[0] * self._dy, self._dx, self._dy)
        self.rect = self.image.get_rect()
        self.move_t = None
        self.frame_ct = 0
        self.speed_x = 0
        self.speed_y = 0
        self.moving_frames = 0


    def update(self, *args):
        if self.moving_frames > 0:
            self.moving_frames -= 1

            self.rect.centerx += self.speed_x
            self.rect.bottom += self.speed_y
            if self.moving_frames == 0:
                self.moving = False

        if self.animate or self.moving:
            ticks = args[0]
            if ticks - self.frame_ct >= self.animate_speed:
                # 运动频率可以通过 animate_speed修改?
                self.frame_ct = args[0]
                # print(self.frame_ct)
                self.face[1] = (self.face[1] + 1) % 2 # self.shape[1]
                # print(self.id, self.face, self.frame_ct)
        elif self.face[1] % 2 == 1:
            self.face[1] = (self.face[1] + 1) % self.shape[1]
        self.image = self.src.subsurface(self.face[1] * self._dx, self.face[0] * self._dy, self._dx, self._dy)

    def change_face(self, spdx, spdy):
        if spdy > 0.1:
            self.face[0] = 0
        elif spdx < -0.1 and self.shape[0] > 1:
            self.face[0] = 1
        elif spdx > 0.1 and self.shape[0] > 2:
            self.face[0] = 2
        elif spdy < -0.1 and self.shape[0] > 3:
            self.face[0] = 3

    # 移动精灵：一般要给出目标位置(默认centerx,bottom)和时间，根据FPS屡次更新完成
    # 实现： 一般在update里反复写  尝试过使用多线程异步完成 但没必要而且时间不好控制
    def move(self, dst, time=100.):
        if self.moving:
            return False
        diff_x = dst[0] - self.rect.centerx
        diff_y = dst[1] - self.rect.bottom
        frames = FPS * time / 1000
        wtime = time / 1000 / frames
        self.speed_x = diff_x / frames
        self.speed_y = diff_y / frames
        self.moving = True
        self.change_face(diff_x, diff_y)
        self.moving_frames = frames
        # 弃用线程
        # self.move_t = threading.Thread(target=move_thread)
        # self.move_t.start()
        return True

    def move_directly(self, dst):
        self.rect.centerx = dst[0]
        self.rect.bottom = dst[1]


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
        self.rect.centerx, self.rect.bottom = temp_trans(pos)

        self.moving = False
        self._walk = 0

    def update(self,*args):  # TODO：坐标系
        self.image = self.src.subsurface(self.face[1] * self._dx, self.face[0] * self._dy, self._dx, self._dy)
        # self.rect = self.image.get_rect()
        dst_pos = temp_trans(self.pos)  # 目标的物理坐标
        cur_pos = rect_trans(self.rect)

        step = int(temp_scale / temp_freq) + int(((temp_scale % temp_freq) * 2 - 1) / temp_freq)

        # 步长算法： 如果有余数且余数大于步长的一半 分配到每一步上 否则之后对齐

        def shiftleg():  # 对齐变腿
            self.face[1] = (self.face[1] + 1) % self.size[1]
            # print("换腿", self.face[1])

        def attention():
            if self.face[1] % 2 == 0:
                return
            else:
                shiftleg()

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

            if 0 < res < 2 * step:
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

        sx = move_axis(cur_pos[0], dst_pos[0], step, temp_scale)  # , shiftleg)
        sy = move_axis(cur_pos[1], dst_pos[1], step, temp_scale)  # , shiftleg)

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
        if self.moving:  # 移动中不接受新指令
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
        # print(self.pos)
        # self.update()

    def move_directly(self, pos):  # 瞬移
        self.pos = pos
        self.rect.centerx, self.rect.bottom = temp_trans(pos)


class Player(EventSprite):
    def __init__(self):
        from os import path
        player_img = pygame.image.load(path.join(img_dir, "hero48.png"))
        self.image = pygame.transform.scale(player_img, (64 * 4, 64 * 4))
        # self.image.set_colorkey(WHITE)
        super().__init__(0, self.image, [4, 4])
        self.speedx = 0
        self.speedy = 0

    def update(self,*args):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.move([self.rect.centerx - BLOCK_UNIT, self.rect.bottom])
        elif keystate[pygame.K_RIGHT]:
            self.move([self.rect.centerx + BLOCK_UNIT, self.rect.bottom])
        elif keystate[pygame.K_UP]:
            self.move([self.rect.centerx, self.rect.bottom - BLOCK_UNIT])
        elif keystate[pygame.K_DOWN]:
            self.move([self.rect.centerx, self.rect.bottom + BLOCK_UNIT])
        # else:
        super().update(*args)
        # print(keystate)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

sp = Player()

if __name__ == '__main__':
    group = pygame.sprite.Group()
    group.add(sp)
    running = True
    while running:
        screen.fill(BLACK)
        group.draw(screen)
        group.update()
        pygame.display.update()

        for event in pygame.event.get():
            # Check for closing window
            if event.type == pygame.QUIT:
                running = False
