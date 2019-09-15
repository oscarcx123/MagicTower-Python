#  图标/静态图块
from lib.utools import *

ICON_DATA = {}

ICON_START_NUM = 300

ICON_IMG = crop_images(load_image("img/icons.png"), ICON_START_NUM, create_rect(32, 32))


def register_icon(img, idnum=None):
    if idnum is None:
        idnum = ICON_START_NUM + len(ICON_IMG)
    ICON_IMG[str(idnum)] = img


def register_icon_crops(image, rect=None, start_num=None):
    w = image.get_rect().w
    if rect is None:
        rect = create_rect(w, w)
    if start_num is None:
        start_num = ICON_START_NUM + len(ICON_IMG)
    temp = crop_images(image, start_num, rect)
    for t in temp:
        ICON_IMG[t] = temp[t]


# !insert! === 在这里注册额外素材 ===
register_icon(load_image("img/ground.png"), idnum=0)
register_icon_crops(load_image("img/walls.png"), start_num=1)
register_icon_crops(load_image("img/shop_LR.png"), start_num=7)
register_icon_crops(load_image("img/doors.png"), start_num=81)
register_icon_crops(load_image("img/stairs.png"), start_num=87)

