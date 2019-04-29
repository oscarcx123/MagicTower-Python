"""

地图ground的demo：

建立需要知道地图逻辑大小w,h（如(13,13)），起始坐标默认0，0，
需要一个全局的资源访问接口，data_dict ，是id到Surface或者Sprite的映射

在地图ground范围内显示的有两类元素（暂不考虑动态图块 视为事件精灵）：
1. 静态图块： 典型元素如墙、道具、…… 直接使用Surface类素材
2. 动态事件： 如怪物、门…… 使用EventSprite(id,configure)生成，其中configure是对该事件动画的配置（素材形状）


TODO： 需要解决surface对底层不透明的问题，目前需要在地图层重绘地板

"""

from lib.ground import GroundSurface
from pygame import Rect, Surface
from .sprite import EventSprite
from lib.utools import *
from sysconf import *
from lib import global_var

class MapGround(GroundSurface):
    def __init__(self, w, h, block_size=32):
        self.block_size = block_size
        self.width = w
        self.height = h
        self.map_data = None
        self.temp_srufcae = None
        super().__init__(0, 0, w * block_size, h * block_size)

    def trans_locate(self, *args):
        """
        逻辑转物理，默认为top left
        :param args:
        :arg[3]: "up":top centerx "down": bottom centerx

        exmaple 1: map.trans_locate(12,12,'down') # 获取坐标 然后在该位置绘制敌人
        example 2: event.move(map.trans_locate(12,12,'down')) # 移动事件到12，12位置

        :return:
        """
        x, y = args[0], args[1]
        if len(args) > 2:
            if args[2] == "up":
                return int((x + 0.5) * self.block_size), y * self.block_size
            elif args[2] == "down":
                return int((x + 0.5) * self.block_size), (y + 1) * self.block_size

        return x * self.block_size, y * self.block_size

    def set_map(self, map_data):
        self.clear_map()
        self.map_data = map_data
        self.draw_map()

    def clear_map(self):
        # self.group.clear()
        self.group.empty()

    def flush(self, screen=None):
        if self.temp_srufcae is not None: # 地图刷新时先直接绘上静态部分
            self.surface.blit(self.temp_srufcae, self.temp_srufcae.get_rect())
        super().flush(screen=screen)
    
    # TODO: 目前显伤放在draw_map里头，因此这里要进行初始化获取get_damage_info函数
    def lib_map_init(self):
        from project.function import get_damage_info
        global get_damage_info
    
    # draw_map 绘制地图，之后刷新不再重绘，除非更新地图状态
    def draw_map(self, map_data=None):
        print("draw map")
        self.clear_map() # 清空精灵
        if map_data is None:
            map_data = self.map_data
        temp_x = 0
        temp_y = 0
        px, py = self.trans_locate(0, 0)
        rect = Rect(px, py, self.block_size, self.block_size)
        ground = get_resource('0')  # 地板 先暂时这么搞吧
        self.fill_surface(ground, mode="repeat")
        PlayerCon = global_var.get_value("PlayerCon")
        self.add_sprite(PlayerCon)
        while temp_y < self.height:
            while temp_x < self.width:
                map_element = map_data[temp_y][temp_x]
                if int(map_element) != 0:
                    # sprite的显示需要接通group
                    name = str(map_element)
                    ret = get_resource(name)
                    px, py = self.trans_locate(temp_x, temp_y, "down")
                    rect.centerx = px
                    rect.bottom = py
                    if type(ret) is tuple:  # 属于精灵 (注意：此时不能直接导入精灵，因为先有map后有精灵）
                        img = ret[0]
                        img_rect = ret[1]  # 以资源本体大小显示 用以支持超过32*32的图像
                        img_rect.topleft = rect.topleft
                        sp = list(ret[2])
                        self.add_sprite(EventSprite(name, img, sp), fill_rect=img_rect)
                    elif ret is not None:
                        self.fill_surface(ret, fill_rect=rect)
                    if map_element > 200:
                        result = get_damage_info(map_element)
                        if result == False:
                            damage = "???"
                        else:
                            damage = result["damage"]
                        self.draw_text(str(damage), 22, WHITE, temp_x, temp_y)
                temp_x += 1
            temp_y += 1
            temp_x = 0
            self.temp_srufcae = self.surface.copy()
    
    # get_block 获取指定地点的图块
    def get_block(self, x, y):
        if self.map_data is not None:
            return self.map_data[y][x]
        else:
            return []
    
    # check_block 获取指定图块的地点，没有则返回空数组
    def check_block(self, target):
        if self.map_data is not None:
            temp_x = 0
            temp_y = 0
            height = int(HEIGHT / BLOCK_UNIT)
            width = int(WIDTH / BLOCK_UNIT) - 4 # -4是因为左边有状态栏
            result = []
            while temp_y < height:
                while temp_x < width:
                    if self.map_data[temp_y][temp_x] == target:
                        result.append([temp_x,temp_y])
                    temp_x += 1
                temp_y += 1
                temp_x = 0
            return result
        else:
            return []
    
    # set_block 设置指定点的图块
    def set_block(self, x, y, target):
        if self.map_data is not None:
            self.map_data[y][x] = target
            
    # remove_block 移除指定点的图块（等价于set_block(x, y, 0)）
    def remove_block(self, x, y):
        if self.map_data is not None:
            self.map_data[y][x] = 0

