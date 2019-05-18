import global_var
import json
import tkinter as tk

# 写入floor_data.json文件
def save_to_file(data=None):
    if data == None:
        data = global_var.get_value("floor_data")
    path = global_var.get_value("floor_data_path")
    with open((path), "w") as f:
        json.dump(data, f)
    status_text = global_var.get_value("status_text")
    status_text.set(f"成功保存到{path}！")

# 读取floor_data.json文件
def read_file(path_entry=None):
    if path_entry is None:
        path = global_var.get_value("floor_data_path")
    else:
        path = path_entry.get()
    status_text = global_var.get_value("status_text")
    try:
        with open(path) as f:
            floor_data = json.load(f)
        global_var.set_value("floor_data", floor_data)
        flush_floor_list()
        status_text.set(f"成功读取{path}！")
        enable_edit()
    except json.decoder.JSONDecodeError:
        status_text.set(f"读取失败，{path}文件为空或者格式不是JSON！")
    except FileNotFoundError:
        status_text.set(f"读取失败，{path}文件不存在！")
    except TypeError:
        status_text.set(f"读取失败，{path} not iterable！")
    except:
        status_text.set(f"读取失败，未知错误！")

# 启用编辑功能（加载地图文件成功）
def enable_edit():
    filemenu = global_var.get_value("filemenu")
    filemenu.entryconfig("保存", state="normal")

# 禁用编辑功能（加载地图文件失败）
def disable_edit():
    filemenu = global_var.get_value("filemenu")
    filemenu.entryconfig("保存", state="disabled")

# 刷新左侧楼层列表
def flush_floor_list():
    floor_listbox = global_var.get_value("floor_listbox")
    floor_data = global_var.get_value("floor_data")
    floor_listbox.delete(0,tk.END)
    for key in floor_data:
        floor_listbox.insert("end", key)
