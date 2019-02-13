#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/5 16:07
# @Author  : dljgs1
# @Site    : 
# @File    : event.py
# @Software: PyCharm
"""
function:
    实现事件流
"""


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

    # 立即执行列表中的事件
    def do_action(self):
        pass

    # 插入一系列事件到当前的列表中
    def insert_action(self, lst):
        if type(lst) is not list:
            lst = [lst]
        self.data_list = lst + self.data_list
