import pygame
from sysconf import *


# 事件原型精灵 用于对事件的蒙皮 也可以暂时当作做动态图块用
# 因为是原型精灵 与地图位置无关 内部坐标仅仅是rect 初始均为0,0
class EventSprite(pygame.sprite.Sprite):
    def __init__(self, id, image, shape, face=None, animate=True):
        """

        :param id: 精灵标识符（暂时无用
        :param image: 动态图
        :param shape: 动态图形状（行数x列数）
        :param face: [0,0]当前朝向、图帧
        :param animate: 是否处于动画中
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
        self.callback = None

    def update(self, *args):
        if self.moving_frames > 0:
            self.moving_frames -= 1
            self.rect.centerx += self.speed_x
            self.rect.bottom += self.speed_y
            if self.moving_frames == 0: # 当前运动结束
                if self.callback is not None:
                    self.callback()
                self.callback = None
                self.moving = False
                return

        if self.animate or self.moving:
            ticks = args[0]
            if ticks - self.frame_ct >= self.animate_speed:
                # 运动频率可以通过 animate_speed修改
                self.frame_ct = args[0]
                self.face[1] = (self.face[1] + 1) % self.shape[1]  # self.shape[1]
                # print(self.id, self.face, self.frame_ct)
        elif self.face[1] % 2 == 1:  # 对齐
            self.face[1] = (self.face[1] + 1) % self.shape[1]
        self.image = self.src.subsurface(self.face[1] * self._dx, self.face[0] * self._dy, self._dx, self._dy)

    def change_face(self, spdx, spdy):
        if abs(spdx) < abs(spdy):
            if spdy < 0 and self.shape[0] > 3:
                self.face[0] = 3
            if spdy > 0:
                self.face[0] = 0
        else:
            if spdx < 0 and self.shape[0] > 1:
                self.face[0] = 1
            elif spdx > 0 and self.shape[0] > 2:
                self.face[0] = 2

    # 移动精灵：一般要给出目标位置(默认centerx,bottom)和时间，根据FPS屡次更新完成
    # 实现： 一般在update里反复写  尝试过使用多线程异步完成 可以使用但没必要而且时间不好控制
    # 移动速度取决于动画时间
    # TODO:在此用时间限定 time: 运动完所需的毫秒数——可能与FPS有关 这里还没做好
    def move(self, dst, time=None, callback=None):
        #if self.moving:
        #    return False
        diff_x = dst[0] - self.rect.centerx
        diff_y = dst[1] - self.rect.bottom
        if time is None:
            time = self.animate_speed / 2
        frames = FPS * time / 1000
        wtime = time / 1000 / frames
        self.speed_x = diff_x / frames
        self.speed_y = diff_y / frames
        self.moving = True
        self.change_face(diff_x, diff_y)
        self.moving_frames = frames
        self.callback = callback
        # 弃用线程
        # self.move_t = threading.Thread(target=move_thread)
        # self.move_t.start()
        return True

    def move_directly(self, dst):
        self.rect.centerx = dst[0]
        self.rect.bottom = dst[1]

