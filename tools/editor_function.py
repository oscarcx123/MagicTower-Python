import global_var
import json
import os
import tkinter as tk

# 写入floor_data.json文件
def save_to_file(**kwargs):
    data = kwargs["data"]
    path = global_var.get_value("floor_data_path")
    file_name = kwargs["file"] + ".json"
    full_path = os.path.join(path, file_name)
    with open((full_path), "w") as f:
        json.dump(data, f)
    status_text = global_var.get_value("status_text")
    if "show_status" in kwargs:
        if kwargs["show_status"] == True:
            status_text.set(f"成功保存到{full_path}！")

# 读取floor_index.json
def read_floor_index(path=None):
    if path == None:
        path = global_var.get_value("floor_data_path")
        floor_index_path = os.path.join(path, "..", "floor_index.json")
    else:
        floor_index_path = path.get()
    status_text = global_var.get_value("status_text")
    try:
        with open(floor_index_path) as f:
            floor_index = json.load(f)
        flush_floor_list(floor_index["index"])
        enable_edit()
        status_text.set(f"读取{floor_index_path}成功！")
    except:
        status_text.set(f"读取{floor_index_path}失败！")

# 启用编辑功能（加载地图文件成功）
def enable_edit():
    filemenu = global_var.get_value("filemenu")
    filemenu.entryconfig("保存", state="normal")

# 禁用编辑功能（加载地图文件失败）
def disable_edit():
    filemenu = global_var.get_value("filemenu")
    filemenu.entryconfig("保存", state="disabled")

# 刷新左侧楼层列表
def flush_floor_list(floor_list):
    floor_listbox = global_var.get_value("floor_listbox")
    floor_listbox.delete(0,tk.END)
    for item in floor_list:
        floor_listbox.insert("end", item)
