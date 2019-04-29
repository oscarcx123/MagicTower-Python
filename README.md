# Python 魔塔样板
## 简介
使用Python的Pygame模块制作的魔塔样板，理论上支持全平台游戏！

**目前的情况来看，完全不会编程的用户，使用起来可能会有一定难度！**

### 其它语言编写的开源魔塔
#### HTML5
* [HTML5样板](https://github.com/ckcz123/mota-js/)
* [HTML5魔塔游戏列表](https://h5mota.com/)
#### C++
* [C++魔塔](https://github.com/ckcz123/mota)

## 更新说明

### 2019.0x.xx V0.6.0 （预先记录）
* [x] 怪物显伤
* [x] 增加全局变量模块
* [x] 将ui.py内容整合到ground类中
* [x] 简陋的开始界面（待完善）
* [x] 简陋的怪物手册（待完善）

当前待处理工作：
* 道具 - 背包UI，具体道具效果代码核查
* 音效
* 存读档 - 界面UI，具体存读档实现


### 2019.04.26 V0.5.1
* [x] 初步完成重构

当前待处理工作：
* 道具 - 背包UI，具体道具效果代码核查
* 怪物手册UI
* 怪物显伤
* 音效
* 存读档 - 界面UI，具体存读档实现
* 开始界面UI


### 2019.02.05 V0.5.0
* [x] 重构大部分显示代码实现以及工程目录分布
* [x] 实现画布系统，树形结构，统一管理，画布内使用相对坐标
* [x] 基于画布的地图显示模块，提供逻辑坐标和地图信息的访问接口，不再直接访问地图数据库
* [x] 素材分类管理，通过get_resource以标识符访问，素材改用带透明通道的png
* [x] 增加事件精灵EventSprite，实现怪物动画
* [x] 实现简单的控制台实时调试 

当前待处理工作：把旧有内容移植到新框架下（旧有部分除了素材目前仍然兼容）


### 2019.02.04 V0.4.0

* [x] 修复若干bugs
* [x] 简单怪物手册实现
* [x] 简单怪物显伤实现
* [x] 完成大部分道具效果

### 2019.02.01 V0.3.1

* [x] 废除get_item函数并改用pick_item函数
* [x] 增加use_item函数
* [x] 引入HTML5魔塔样板的item数据并存放到items.py
* [x] 完成部分道具的实现
* [x] 将地图数据分离到tower_map.py
* [x] 将怪物数据分离到monster.py
* [x] 将地图数据映射表分离到id_map.py
* [x] 废除tower_database.py

### 2019.01.31 V0.3.0

* [x] 添加ActorSprite
* [x] 实现勇士动态行走图
* [x] 补全get_item函数
* [x] 完成不同函数间坐标的对接
* [x] 移动所有常数到sysconf.py
* [x] 修复crop_image函数切图错误
* [x] 修复get_damage_info函数破防判断错误
* [x] 本次自带demo取自《生命之林》魔塔的一部分

### 2019.01.29 V0.2.0

* [x] 实现上下楼以及开门的处理
* [x] 增加change_floor函数
* [x] 增加open_door函数
* [x] 增加check_map函数

### 2019.01.29 V0.1.0

* [x] 增加crop_image函数

### 2019.01.28 V0.0.1

* [x] 发布初版Python魔塔样板的雏形

---------------------------

# MagicTower-Python
## Intro
Magic Tower written in Python

### Other Open Source Magic Towers
#### HTML5
* [HTML5 Magic Tower Template](https://github.com/ckcz123/mota-js/)
* [HTML5 Magic Tower Games](https://h5mota.com/)
#### C++
* [C++ Magic Tower](https://github.com/ckcz123/mota)
