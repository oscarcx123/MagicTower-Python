"""
消息注册机制，基于pygame.event
使用方法：
action_control = global_var.get_value("action_control")
action_control.register_action(name, type, callback, priority) # 注册对一个event.type为type的事件的监听

"""
import pygame


class Action:
    def __init__(self, name, type, callback, priority=0):
        self.name = name
        self.type = type
        self.fun = callback
        self.priority = priority

    def do_fun(self, event):
        return self.fun(event)


class ActionControl:
    def __init__(self):
        self.listen_list = {}

    def register_action(self, name, listen_type=None, listen_fun=None, priority=0):
        if type(name) is str:
            action = Action(name, listen_type, listen_fun, priority)
        else:
            action = name
        if listen_type not in self.listen_list:
            self.listen_list[listen_type] = []
        for a in self.listen_list[listen_type]:
            if a.name == action.name:
                self.listen_list[listen_type].remove(a)
        self.listen_list[listen_type].append(action)
        self.listen_list[listen_type].sort(key=lambda it: it.priority, reverse=True)

    def action_render(self):
        for event in pygame.event.get():
            if event.type in self.listen_list:
                for action in self.listen_list[event.type]:
                    if action.do_fun(event):
                        break