import pygame
from lib import CurrentMap
from .sprite import EventSprite
from sysconf import *
from lib import global_var

# 玩家控制逻辑：
class Player(EventSprite):
    def __init__(self):
        from os import path
        player_img = pygame.image.load(path.join(img_dir, "hero48.png"))
        self.image = pygame.transform.scale(player_img, (int(BLOCK_UNIT * 4), int(BLOCK_UNIT * 4)))
        # self.image.set_colorkey(WHITE)
        super().__init__(0, self.image, [4, 4])
        self.reset()

    # 重置/初始化角色数据
    def reset(self):
        self.speedx = 0
        self.speedy = 0
        self.pos = [X_COORDINATE, Y_COORDINATE]
        self.floor = PLAYER_FLOOR
        self.visited = [CurrentMap.floor_index["index"][self.floor]] # 玩家已经去过的楼层，默认去过起始楼层
        self.lock = False
        self.key_pressed = False
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
        self.var = {}
        self.FUNCTION = global_var.get_value("FUNCTION")

    # TODO：各种block的处理
    def proc_block(self, block_id, x, y):
        if [x, y] in CurrentMap.event_data:
            EVENTFLOW = global_var.get_value("EVENTFLOW")
            EVENTFLOW.add_action(x, y)
        elif block_id == "onSide":
            return False
        # block_id = 0 -> 空地
        elif int(block_id) == 0:
            return True
        # block_id = 1-5 -> 各类墙
        elif int(block_id) >= 1 and int(block_id) <= 5:
            return False
        # block_id = 21~69 -> 道具
        elif int(block_id) >= 21 and int(block_id) <= 69:
            self.FUNCTION.pickup_item(block_id, x, y)
            return True
        # block_id = 81~86 -> 门
        elif int(block_id) >= 81 and int(block_id) <= 86:
            # 快速存档
            self.FUNCTION.save()
            result = self.FUNCTION.open_door(block_id, x, y)
            if result == False:
                return False
        # block_id = 87~88 -> 楼梯
        elif int(block_id) == 87 or int(block_id) == 88:
            result = self.FUNCTION.change_floor(block_id)
            return False
        # block_id = 201+ -> 怪物
        elif int(block_id) >= 201:
            result = self.FUNCTION.get_damage_info(block_id)
            if result["status"] == True and result["damage"] < self.hp:
                # 快速存档
                self.FUNCTION.save()
            result = self.FUNCTION.battle(block_id, x, y, result=result)
            if result == False:
                return False
        return False

    def update(self, *args):
        EVENTFLOW = global_var.get_value("EVENTFLOW")
        while len(EVENTFLOW.data_list) > 0 and not self.lock and not EVENTFLOW.wait_finish:
            EVENTFLOW.do_event()
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        key_map = {pygame.K_LEFT: [-1, 0],
                   pygame.K_RIGHT: [1, 0],
                   pygame.K_UP: [0, -1],
                   pygame.K_DOWN: [0, 1],
                   pygame.K_z: "change_face",
                   pygame.K_a: "load_auto",
                   pygame.K_b: "text_demo"} # text_demo暂时跟B键绑定在一起，方便测试文本框
        if not self.moving and not self.lock:
            for k in key_map:
                op = key_map[k]
                # 一次只响应一个按键，由self.key_pressed控制
                if keystate[k] and not self.key_pressed:
                    self.key_pressed = True
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
                        if op == "change_face":
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
                        # 文本框测试（B键触发）
                        elif op == "text_demo":
                            TEXTBOX = global_var.get_value("TEXTBOX")
                            TEXTBOX.show("欢迎来到python魔塔样板v0.9\n1. 本窗口使用TextBox包装，内部调用使用TextWin，字体默认36号，字数自适应。\n2. 实现更多窗口使用WinBase，目前只能做文字显示，后续补充选择光标和图像以及计算式\n3. 事件触发可以考虑用列表\n4. 文本解析也许比较费时？可以考虑先解析\n5. 更多乱七八糟的功能还在开发中。。。。。。\n目前写得乱七八糟，因为目标是先能用再说，以后肯定需要重构下的。\nby Azure（蓝皮鼠） & dljgs1（君浪）\n以下是测试内容：\n目前实现了文本框的自适应。\n当前设定的最大行数为10。\n可以看到，当文字行数超过10之后，文本框会自动截断，按回车键之后继续展示。\n如果需要展示的文字数量特别多，TextBox能够将文本每十行截断一次，并且文本框高度为自适应！\n那么接下来要演示的就是最后的自适应部分。\n由于画布在创建后无法随意调整大小，因此这里的技术原理就是获取剩下需要展示的文字list，然后计算出需要的文本框高度，最后创建一个新的对象用于覆盖旧的对象，这样就可以重新设定画布的大小。")
                        elif op == "load_auto":
                            self.FUNCTION.load()
                            pygame.time.wait(250)
            self.key_pressed = False
        super().update(*args)

    def get_face(self):
        return self.face[0]

    def change_hero_loc(self, x, y):
        self.move_directly(CurrentMap.trans_locate(x, y, "down"))
        self.pos = [x, y]
