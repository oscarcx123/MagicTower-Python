# 这里放各种独立的工具
import pygame


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
    while rect.bottom < img_rect.bottom:
        while rect.left <= rect.right - rect.w:
            data_dict[str(start_num)] = image.subsurface(rect)
            rect.left += rect.w
            start_num += 1
        rect.left = 0
        rect.bottom += rect.h
    return data_dict


def load_image(path):
    return pygame.image.load(path)


def create_rect(w, h):
    return pygame.Rect(0, 0, w, h)


# !insert! === 在这里编写自定义工具函数 ===
