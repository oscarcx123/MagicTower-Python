# 窗口基类 - 实现winskin以窗口形式展示
import pygame
from pygame import Surface
from pygame.sprite import Sprite
from pygame.transform import scale

# 基本配置 可以放到sysconf：
winSkinPath = "img/winskin.png"

from pygame import Rect


class WinBase(Sprite):
    def __init__(self, w, h, x, y, dir=None):
        super().__init__()
        self.src = pygame.image.load(winSkinPath)
        self.pos = [x, y]  # windows的坐标就是物理坐标 left、top
        self.show = False
        self.src_show = self.init_wind(w, h, dir)

        self.image = self.src_show  # Surface([w, h])
        self.rect = self.image.get_rect()

    def trans_image(self, params):  # 把原图转成设备显示的surface
        if len(params) == 3:
            print(params)
            return scale(self.src.subsurface(params[0]), params[1]), params[2]
        else:
            return self.src.subsurface(params[0]), params[1]

    def init_wind(self, w, h, dir):

        x, y = self.pos[0], self.pos[1]
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

    def turn_off(self):
        pass

    def update(self, *args):
        if not self.show:
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(0.9)
            # self.image = self.src_show
            # self.rect = self.image.get_rect()
