from lib.utools import *

ITEMS_DATA = {}  # TODO： 写各个物品的类别或效果
ITEMS_START_NUM = 21  # ??我不知道
ITEMS_IMG = crop_images(load_image("img/items.png"),ITEMS_START_NUM,create_rect(32, 32))

# !insert! === 在这里注册额外物品（items.png之外的特殊素材） ===
