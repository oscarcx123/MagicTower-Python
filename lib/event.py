from lib import global_var
import re

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



class EventFlow:
    def __init__(self):
        self.data_list = []  # 当前在执行的事件列表
        self.auto = False  # 自动执行中
        self.wait_key = None  # 等待驱动的关键按钮
        self.PlayerCon = global_var.get_value("PlayerCon")
        self.CurrentMap = global_var.get_value("CurrentMap")

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
            self.CurrentMap.event_data.remove([x, y])
            return flow

    def do_event(self):
        TEXTBOX = global_var.get_value("TEXTBOX")
        for event in self.data_list:
            if not self.PlayerCon.lock:
                self.data_list.pop(0)
                if type(event) is dict:

                    event_type = event["type"]
                    if event_type == "if":
                        condition = event["condition"]
                        cond_is_reversed = False
                        is_flag = False
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
                        if "flag:" in condition:
                            condition = condition.lstrip("flag:")
                            is_flag = True
                        if is_flag:
                            cond_eval_result = condition in self.PlayerCon.flag
                        if cond_is_reversed:
                            cond_eval_result = not cond_eval_result
                        if cond_eval_result == True:
                            self.insert_action(event["true"])
                        else:
                            self.insert_action(event["false"])
                    else:
                        TEXTBOX.show(f"暂时无法解析：{event}")
                elif type(event) is str:
                    TEXTBOX.show(event)
                else:
                    TEXTBOX.show(f"暂时无法解析：{event}")
            else:
                break

                        


        


