from lib import global_var, WriteLog
import re
import pygame

# 事件基本单元
class Event:
    """
    事件类型（cls）：
        control - 控制流 if while 等
        data - 数据操作
        show - 显示操作

    """
    def __init__(self):
        self.cls = '' # 类型： 逻辑/显示
        self.PlayerCon = global_var.get_value("PlayerCon")
        self.CurrentMap = global_var.get_value("CurrentMap")
        self.TEXTBOX = global_var.get_value("TEXTBOX")
        self.BlockDataReverse = global_var.get_value("BlockDataReverse")
        self.Music = global_var.get_value("Music")
        self.FUNCTION = global_var.get_value("FUNCTION")


    def get_event_flow_module(self):
        self.EVENTFLOW = global_var.get_value("EVENTFLOW")

    # 显示一段文字
    def text(self, event):
        # 正则匹配\t[.....]
        result = re.match("\\t\[\S*\]", event)
        if result is not None:
            header = result.group()
            event = event.lstrip(header)
            header = header.lstrip("\t[")
            header = header.rstrip("]")
            header = header.split(",")
            if len(header) == 1:
                name = header[0]
                event = name + "\n" + event
            if len(header) == 2:
                name = header[0]
                icon = header[1]
                # TODO: 显示icon
                event = name + "\n" + event
        self.TEXTBOX.show(event)

    # if条件判断
    def if_cond(self, event):
        condition = event["condition"]
        cond_is_reversed = False
        # 正则匹配!(......)
        result = re.match("!\(\S*\)", condition)
        if result is not None:
            cond_is_reversed = not cond_is_reversed
            condition = condition.lstrip("!(")
            condition = condition.rstrip(")")
        # 正则匹配(!......)
        result = re.match("\(!\S*\)", condition)
        if result is not None:
            cond_is_reversed = not cond_is_reversed
            condition = condition.lstrip("(!")
            condition = condition.rstrip(")")         
        cond_eval_result = condition in self.PlayerCon.var
        if cond_is_reversed:
            cond_eval_result = not cond_eval_result
        if cond_eval_result:
            self.EVENTFLOW.insert_action(event["true"])
        else:
            self.EVENTFLOW.insert_action(event["false"])

    def parse_value(self, value):
        if "core.itemCount" in value:
            value = value.replace("core.itemCount", "self.FUNCTION.count_item")
        return eval(value)

    # 设置玩家属性，道具数量，或者变量的值
    def set_value(self, event):
        event_type = event["type"]
        value_name = event["name"]
        value = self.parse_value(event["value"])
        if "flag:" in value_name or "switch:" in value_name:
            # TODO: 独立开关需要进一步处理，否则无法识别不同事件的独立开关
            if event_type == "setValue":
                self.PlayerCon.var[value_name] = value
            elif event_type == "addValue":
                if value_name in self.PlayerCon.var:
                    self.PlayerCon.var[value_name] += value
                else:
                    self.PlayerCon.var[value_name] = value
        elif "status:" in value_name:
            value_name = value_name.lstrip("status:")
            command = "self.PlayerCon." + value_name
            if event_type == "setValue":
                command = command + "=" + str(value)
            elif event_type == "addValue":
                command = command + "+=" + str(value)
            exec(command)
        elif "item:" in value_name:
            value_name = value_name.lstrip("item:")
            if value_name in self.BlockDataReverse:
                map_obj_id = int(self.BlockDataReverse[value_name])
                if event_type == "setValue":
                    self.FUNCTION.set_item_amount(map_obj_id, value)
                elif event_type == "addValue":
                    self.FUNCTION.add_item(map_obj_id, value) 
            else:
                self.TEXTBOX.show(f"请检查{value_name}是否正确")
                print(f"请检查{value_name}是否正确")
        else:
            self.TEXTBOX.show(f"暂时无法解析：{event}")
            print(f"暂时无法解析：{event}")
        self.FUNCTION.flush_status()

    # 打开全局商店
    def open_shop(self, event):
        shop_id = event["id"]
        chosen_shop = global_var.get_value(shop_id)
        chosen_shop.open()

    # 播放音效
    def play_sound(self, event):
        sound_name = event["name"]
        self.Music.play_SE(sound_name)

    # 开门
    def open_door(self, event):
        loc = event["loc"]
        x = loc[0]
        y = loc[1]
        if "floorId" in event:
            floor_id = event["floorId"]
        else:
            floor_id = self.CurrentMap.get_floor_id(self.PlayerCon.floor)
        self.CurrentMap.MAP_DATABASE[floor_id]["map"][y][x] = 0

    # 等待一段时间（单位是毫秒）
    def sleep(self, event):
        sleep_time = int(event["time"])
        pygame.time.wait(sleep_time)

    # 呼出存档界面
    def call_save(self, event):
        save = global_var.get_value("SAVE")
        save.open()

    # 呼出选项框
    def choices(self, event):
        text = event["text"]
        choices = event["choices"]
        ChoiceBox = global_var.get_value("CHOICEBOX")
        ChoiceBox.init(text, choices)
        ChoiceBox.open()

    # 弹出确认框（本质上是只有两个选项的选项框）
    def confirm(self, event):
        text = event["text"]
        choices = [{},{}]
        choices[0]["text"] = "是"
        choices[0]["action"] = event["yes"]
        choices[1]["text"] = "否"
        choices[1]["action"] = event["no"]
        ChoiceBox = global_var.get_value("CHOICEBOX")
        ChoiceBox.init(text, choices)
        ChoiceBox.open()

    # 自定义函数（没有特别好的通用解决办法，尽量避免使用）
    def function(self, event):
        functions = event["function"]
        functions = functions.lstrip("function(){")
        functions = functions.lstrip() # 去除句首\n
        functions = functions.rstrip("}")
        functions = functions.split("\n")
        for item in functions:
            if len(item) != 0:
                convert = {
                    "core.status.hero.hp": "self.PlayerCon.hp",
                    "core.status.hero.atk": "self.PlayerCon.attack",
                    "core.status.hero.def": "self.PlayerCon.defend",
                    "core.status.hero.mdef": "self.PlayerCon.mdefend"
                }
                for convertible in convert:
                    if convertible in item:
                        item = item.lstrip(convertible)
                        item = convert[convertible] + item
                        exec(item)
                        extra_command = convert[convertible] + " = int(" + convert[convertible] + ")"
                        exec(extra_command)
                        return True
                self.TEXTBOX.show(f"暂时无法解析：{event}")
                print(f"暂时无法解析：{event}")
            else:
                self.TEXTBOX.show(f"暂时无法解析：{event}")
                print(f"暂时无法解析：{event}")

    # 游戏胜利事件
    def win(self, event):
        reason = event["reason"]
        score = str(self.PlayerCon.hp)
        text = reason + "\n" + "你的分数是" + score + "。"
        self.TEXTBOX.show(text)
        self.EVENTFLOW.insert_action({"type": "restart"})

    # 强制战斗
    def battle(self, event):
        mon_id = event["id"]
        map_obj_id = int(self.BlockDataReverse[mon_id])
        self.FUNCTION.battle(map_obj_id, enforce=True)

    # 回到标题界面
    def restart(self, event):
        self.FUNCTION.restart()

class EventFlow:
    def __init__(self):
        self.data_list = []  # 当前在执行的事件列表
        self.auto = False  # 自动执行中
        self.wait_key = None  # 等待驱动的关键按钮
        self.PlayerCon = global_var.get_value("PlayerCon")
        self.CurrentMap = global_var.get_value("CurrentMap")
        self.TEXTBOX = global_var.get_value("TEXTBOX")

    def get_event_module(self):
        self.EVENT = global_var.get_value("EVENT")

    # 立即执行列表中的事件
    def do_action(self):
        self.data_list.pop(0)
        # TODO: 执行事件

    # 把事件放到当前队列的末尾
    def add_action(self, x, y, floor=None):
        lst = self.get_event_list(x, y)
        if type(lst) is not list:
            lst = [lst]
        self.data_list = self.data_list + lst

    # 插入一系列事件到当前的列表中
    def insert_action(self, lst):
        if type(lst) is not list:
            lst = [lst]
        self.data_list = lst + self.data_list

    def get_event_list(self, x, y, floor=None):
        if floor is None:
            floor = self.PlayerCon.floor
        if floor == self.PlayerCon.floor:
            flow = self.CurrentMap.get_event_flow(x, y, floor)
            if type(flow) is dict and len(flow) == 5:
                if "data" in flow:
                    flow = flow["data"]
            # self.CurrentMap.event_data.remove([x, y]) 这句不启用，因为事件可以反复触发，除非被隐藏
            return flow

    def do_event(self):
        if not self.PlayerCon.lock:
            event = self.data_list[0]
            WriteLog.debug(__name__, "当前执行事件：" + str(self.data_list[0]))
            self.data_list.pop(0)
            if type(event) is dict:
                event_type = event["type"]
                if event_type == "if":
                    self.EVENT.if_cond(event)
                elif event_type == "setValue" or event_type == "addValue":
                    self.EVENT.set_value(event)
                elif event_type == "openShop":
                    self.EVENT.open_shop(event)
                elif event_type == "openDoor":
                    self.EVENT.open_door(event)
                elif event_type == "playSound":
                    self.EVENT.play_sound(event)
                elif event_type == "sleep":
                    self.EVENT.sleep(event)
                elif event_type == "callSave":
                    self.EVENT.call_save(event)
                elif event_type == "choices":
                    self.EVENT.choices(event)
                elif event_type == "confirm":
                    self.EVENT.confirm(event)
                elif event_type == "function":
                    self.EVENT.function(event)
                elif event_type == "win":
                    self.EVENT.win(event)
                elif event_type == "battle":
                    self.EVENT.battle(event)
                elif event_type == "restart":
                    self.EVENT.restart(event)
                else:
                    self.TEXTBOX.show(f"暂时无法解析：{event}")
                    print(f"暂时无法解析：{event}")
            elif type(event) is str:
                self.EVENT.text(event)
            else:
                self.TEXTBOX.show(f"暂时无法解析：{event}")
                print(f"暂时无法解析：{event}")
