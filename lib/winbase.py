# 窗口基类 - 实现winskin以窗口形式展示
import pygame
from pygame import Surface
from pygame.sprite import Sprite
from pygame.transform import scale

# 基本配置 可以放到sysconf：
winSkinPath = "img/winskin.png"

from pygame import Rect

from sysconf import WIDTH, HEIGHT
import re

dw_pattern = re.compile("[\x00-\xff]", re.A)  # 匹配半角字符


class WinBase(Sprite):
    def __init__(self, x, y, w, h, dir=None):
        super().__init__()
        self.src = pygame.image.load(winSkinPath).convert_alpha()
        self.pos = [x, y]  # windows的坐标就是物理坐标 left、top
        self.show = False
        self.src_show = self.init_wind(w, h, dir)
        self.dir = dir

        self.image = self.src_show  # Surface([w, h])
        self.rect = self.image.get_rect()
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]
        print("st", self.rect)
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


font_name = "resource/simhei.ttf"  # pygame.font.SysFont("宋体", 50)

# ---- 局部配置（只用于本文件内容的写在这里） ----
TEXT_WIN_WIDTH = WIDTH - 40
TEXT_WIN_HEIGHT = int(HEIGHT / 4)
TEXT_WIDTH = TEXT_WIN_HEIGHT - 40
TEXT_HEIGHT = TEXT_WIN_HEIGHT - 40
TEXT_LEFT_BOARD = 40  # 侧边距
TEXT_TOP_BOARD = 34  # 顶边距
WHITE = (255, 255, 255)


class TextWin(WinBase):
    def __init__(self, type, content=None,is_talk=False):
        x = (WIDTH - TEXT_WIN_WIDTH) / 2
        y = 0  # 默认贴边
        w = TEXT_WIN_WIDTH
        h = TEXT_WIN_HEIGHT
        self.is_talk = is_talk
        if type == "mid":
            y = int(HEIGHT / 2 - TEXT_WIN_HEIGHT / 2)
        elif type == "down":
            y = HEIGHT - TEXT_WIN_HEIGHT
        elif type == "auto":
            pass
            # TODO： 显示在头上的对话框 & 根据坐标/字数自适应大小对话框
            # 需要建立一个界面地图坐标转换接口，并且把各个界面分离开来
        print(x, y, w, h)
        super().__init__(x, y, w, h)
        self.content = ""
        self.res_content = None

        if content is not None:
            self.content = content
            self.drawText()


    def _calcu_text_list(self):
        pass

    def drawText(self, size=36, content=None):
        if content is None:
            content = self.content

        w = self.rect.w
        h = self.rect.h
        font = pygame.font.Font(font_name, size)

        dw = font.render("字", True, WHITE).get_rect().w  # 全角宽
        # TODO: 直接由size推断出宽度?

        dh = font.get_height()  # font.get_sized_descender()
        line_len = int((w - 2 * TEXT_LEFT_BOARD) / dw)  # 行长
        line_num = int((h - 2 * TEXT_TOP_BOARD) / dh)
        print("行长：%d 行数： %d" % (line_len, line_num))

        # text_len = len(content) + len(dw_pattern.findall(content))
        # if line_num * line_len > text_len:
        #    self.res_content = content[line_num * line_len + 1:]
        #    content = content[0:line_num * line_len]

        line_list = []

        def get_real_len(s):
            return len(s) - int(len(dw_pattern.findall(s)) * 0.5 + 0.6)

        def align_char(content):
            clen = 0
            line = ""
            while clen < line_len and content != '':
                tlen = line_len - clen
                print(tlen)
                tstr = content[:tlen]
                line += tstr
                clen += get_real_len(tstr)
                content = content[tlen:]
            if content != '' and get_real_len(content) <= 2:
                line += content
            print("对齐长度：", get_real_len(line))
            return line

        for content in content.split('\n'):
            while content != '':
                s = align_char(content)
                line_list.append(s)
                content = content[len(s):]

        if len(line_list) > line_num:
            self.res_content = '\n'.join(line_list[line_num:])
            print("res", self.res_content)
            line_list = line_list[:line_num]

        ct = 0
        for text in line_list:
            text_surface = font.render(text, True, WHITE)
            text_rect = text_surface.get_rect()
            print(text_rect)
            text_rect.left = TEXT_LEFT_BOARD  # self.pos[0]
            text_rect.top = TEXT_TOP_BOARD + ct * dh  # + self.pos[1]
            self.src_show.blit(text_surface, text_rect)
            ct += 1

    def updateText(self):
        print("self.res_content", self.res_content)
        if self.res_content is not None:
            self.content = self.res_content
            self.res_content = None
            self.flush_skin()
            self.drawText()
        else:
            self.show_off()

    def update(self, *args):
        super().update(args)
