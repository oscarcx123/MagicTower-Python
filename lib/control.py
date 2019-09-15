import pygame
from lib import CurrentMap
from .sprite import EventSprite
from sysconf import *
from project.function import *

# 玩家控制逻辑：
class Player(EventSprite):
    def __init__(self):
        from os import path
        player_img = pygame.image.load(path.join(img_dir, "hero48.png"))
        self.image = pygame.transform.scale(player_img, (int(BLOCK_UNIT * 4), int(BLOCK_UNIT * 4)))
        # self.image.set_colorkey(WHITE)
        super().__init__(0, self.image, [4, 4])
        self.speedx = 0
        self.speedy = 0
        self.pos = [X_COORDINATE, Y_COORDINATE]
        self.floor = PLAYER_FLOOR
        self.visited = [CurrentMap.floor_index["index"][self.floor]] # 玩家已经去过的楼层，默认去过起始楼层
        self.lock = False
        map_pos = CurrentMap.trans_locate(*self.pos, "down")
        self.rect.centerx = map_pos[0]
        self.rect.bottom = map_pos[1]
        self.animate_speed = PLAYER_SPEED  # 移动一格所需要的毫秒数 & 换腿所需时间的两倍
        self.animate = False
        self.hp = PLAYER_HP
        self.attack = PLAYER_ATK
        self.defend = PLAYER_DEF
        self.mdefend = PLAYER_MDEF
        self.gold = PLAYER_GOLD
        self.exp = PLAYER_EXP
        self.floor = PLAYER_FLOOR
        self.item = PLAYER_ITEM

    # TODO：各种block的处理
    def proc_block(self, block_id, x, y):
        # block_id = 0 -> 空地
        if int(block_id) == 0:
            return True
        if block_id == "onSide":
            return False
        # block_id = 1-5 -> 各类墙
        if int(block_id) >= 1 and int(block_id) <= 5:
            return False
        # block_id = 21~69 -> 道具
        elif int(block_id) >= 21 and int(block_id) <= 69:
            pickup_item(block_id, x, y)
            return True
        # block_id = 81~86 -> 门
        elif int(block_id) >= 81 and int(block_id) <= 86:
            result = open_door(block_id, x, y)
            if result == False:
                return False
        # block_id = 87~88 -> 楼梯
        elif int(block_id) == 87 or int(block_id) == 88:
            result = change_floor(block_id)
            return False
        # block_id = 131 -> 蓝色商店（商店1）
        elif int(block_id) == 131:
            SHOP1 = global_var.get_value("SHOP1")
            SHOP1.open()
            return False
        # block_id = 130 -> 粉色商店（商店2）
        elif int(block_id) == 130:
            SHOP2 = global_var.get_value("SHOP2")
            SHOP2.open()
            return False
        # block_id = 201+ -> 怪物
        elif int(block_id) >= 201:
            result = battle(block_id, x, y)
            if result == False:
                return False
        return False

    def update(self, *args):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        key_map = {pygame.K_LEFT: [-1, 0],
                   pygame.K_RIGHT: [1, 0],
                   pygame.K_UP: [0, -1],
                   pygame.K_DOWN: [0, 1],
                   pygame.K_z: "change_face"}
        if not self.moving and not self.lock:
            for k in key_map:
                op = key_map[k]
                if keystate[k]:
                    if type(op) is list:
                        if not self.proc_block(CurrentMap.get_block(self.pos[0] + op[0], self.pos[1] + op[1]), self.pos[0] + op[0], self.pos[1] + op[1]):
                            self.change_face(*op)
                        else:
                            x = op[0] + self.pos[0]
                            y = op[1] + self.pos[1]

                            def temp_fun():
                                self.pos = [x, y]

                            self.move(CurrentMap.trans_locate(x, y, "down"), callback=temp_fun)
                    elif type(op) is str:
                        # face[0]调用勇士朝向 0=下，1=左，2=右，3=上
                        face = self.get_face()
                        face_map = {
                            0:1,
                            1:3,
                            3:2,
                            2:0
                        }
                        self.face[0] = face_map[face]
                        pygame.time.wait(self.animate_speed)

        super().update(*args)

    def get_face(self):
        return self.face[0]

    def change_hero_loc(self, x, y):
        self.move_directly(CurrentMap.trans_locate(x, y, "down"))
        self.pos = [x, y]


#
