# 这里放各种独立的工具
import pygame
import time
from sysconf import *


def crop_images(image, start_num, rect):
    """
    切分图像 | 用于切取同型图像，如[[AB][CD]]或[ABCD]
    :param image: 原素材图像（surface）
    :param start_num: 开始的编号
    :param rect: 需要切掉获取的图像形状
    :return: 图像字典{"id":Surface}
    :! 取消了prefix——编号直接作为资源索引
    """
    data_dict = {}
    img_rect = image.get_rect()
    while rect.bottom <= img_rect.bottom:
        while rect.right <= img_rect.right:
            print(image.get_rect(), rect)
            data_dict[str(start_num)] = image.subsurface(rect)
            rect.left += rect.w
            start_num += 1
        rect.left = 0
        rect.bottom += rect.h
    return data_dict


# 载入图像用这个 可以提前变换尺寸
def load_image(path):
    img = pygame.image.load(path).convert_alpha() # 保证能使用透明通道
    return pygame.transform.scale(img, (int(img.get_width() * RESOURCE_SCALE),
                                        int(img.get_height() * RESOURCE_SCALE)))


def create_rect(w, h):
    return pygame.Rect(0, 0, w, h)


from project.enemy import MONSTER_IMG
from project.icons import ICON_IMG
from project.items import ITEMS_IMG
from project.npc import NPC_IMG


# 资源接口 根据配置设置返回值
def get_resource(sid):
    if sid in MONSTER_IMG:
        return MONSTER_IMG[sid], MONSTER_IMG[sid].get_rect(), (1, 2)
    if sid in NPC_IMG:
        return NPC_IMG[sid], NPC_IMG[sid].get_rect(), (1, 2)
    if sid in ICON_IMG:
        return ICON_IMG[sid]
    if sid in ITEMS_IMG:
        return ITEMS_IMG[sid]


def get_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

# !insert! === 在这里编写自定义工具函数 ===
