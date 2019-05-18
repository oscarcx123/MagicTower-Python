import tkinter as tk
import tkinter.messagebox
from functools import partial
import os
import json
from editor_function import *
import global_var

'''
全局变量列表：
floor_data = JSON格式的楼层数据
floor_data_path = 楼层数据文件路径
floor_listbox = 编辑器主界面左下的楼层列表
filemenu = 菜单栏的“文件”菜单
status_text = 状态栏
'''

class MainWindow(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.font = ("Arial",12)
        self.floor_data = None
        global_var.set_value("floor_data", self.floor_data)
        # 菜单栏
        # menubar
        self.menubar = tk.Menu(self)

        # menubar > filemenu
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="文件", menu=self.filemenu)
        self.filemenu.add_command(label="新建", command=self.new_ui)
        self.filemenu.add_command(label="加载", command=self.load_ui)
        self.filemenu.add_command(label="保存", command=save_to_file)
        self.filemenu.add_command(label="测试", command=self.test_function)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="退出", command=self.quit)
        global_var.set_value("filemenu", self.filemenu)
        
        # menubar > filemenu > submenu
        # self.submenu = tk.Menu(self.filemenu)
        # self.filemenu.add_cascade(label="TODO", menu=self.submenu, underline=0)
        # self.submenu.add_command(label='TODO', command=self.do_job)

        # menubar > editmenu
        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="帮助", menu=self.editmenu)
        self.editmenu.add_command(label="关于", command=self.about_ui)
        
        # 显示menubar
        global root
        root.config(menu=self.menubar)
        
        # 底部状态栏
        self.status_text = tk.StringVar()
        global_var.set_value("status_text", self.status_text)
        self.status_label = tk.Label(self, textvariable=self.status_text, bg="white", font=("Arial", 12), anchor="w")
        self.status_label.pack(side="bottom", fill=tk.X)
        
        # 显示界面分区
        self.frame_left = tk.Frame(self)
        self.frame_right = tk.Frame(self)
        self.frame_left.pack(side="left", fill=tk.BOTH, expand=1)
        self.frame_right.pack(side="right", fill=tk.BOTH, expand=1)
        
        # 左上图片素材选择
        self.resource_area = tk.Text(self.frame_left, font=self.font, width=36, height=10)
        self.resource_area.insert(tk.END, "TODO: 这里用来显示素材")
        self.resource_area.pack(side="top", fill=tk.BOTH, expand=1)
        
        # 左下楼层列表
        self.floor_list = tk.StringVar()
        self.floor_list.set([])
        self.floor_listbox = tk.Listbox(self.frame_left, listvariable=self.floor_list, font=self.font)
        self.floor_listbox.pack(side="top", fill=tk.BOTH, expand=1)
        self.floor_listbox.bind('<Double-Button-1>', self.edit_floor_data_ui)
        global_var.set_value("floor_listbox", self.floor_listbox)
        
        # 右侧地图显示
        self.map_area = tk.Text(self.frame_right, font=self.font)
        self.map_area.insert(tk.END, "TODO: 这里用来显示地图")
        self.map_area.pack(side="top", fill=tk.BOTH, expand=1)
        
        # 生成默认地图数据文件路径
        self.floor_data_path = os.path.abspath(os.path.join(os.getcwd(), "..", "project", "floor_data.json"))
        global_var.set_value("floor_data_path", self.floor_data_path)
        
        # 默认禁用编辑，成功读取地图数据文件后会自动解禁
        disable_edit()
        
        # 自动尝试在启动时读取地图数据文件
        read_file()
        
    # 空函数，相当于pass    
    def do_job(self, *args):
        print(*args)
        print("Success!")
    
    # 助 > 关于    
    def about_ui(self):
        window = About(self)
    
    # 文件 > 新建
    def new_ui(self):
        window = CreateNewFloor(self)
    
    # 文件 > 加载
    def load_ui(self):
        window = LoadFloor(self)

    # 编辑楼层信息    
    def edit_floor_data_ui(self, *args):
        window = FloorEditor(self)

    # 测试用空窗口
    def test_function(self):
        window2 = BaseWindow(self)

# 空白窗口基类
class BaseWindow():
    def __init__(self, window):
        self.t = tk.Toplevel(window)
        self.font = ("Arial",12)
        self.drawUI()
    
    def drawUI(self):
        self.t.title(f"Window")
        self.l = tk.Label(self.t, text=f"This is a new window")
        self.l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
       
# 关于
class About(BaseWindow):
    def drawUI(self):
        self.t.title("关于")
        self.t.geometry("500x300")
        
        self.l = tk.Label(self.t, text="Python魔塔地图数据编辑器", bg="azure", font=self.font, width=15, height=2)
        self.l.pack(side="top", fill=tk.X)
        
        self.l2 = tk.Label(self.t, text="开发者：Azure & dljgs1", font=self.font, width=15, height=2)
        self.l2.pack(side="top", fill=tk.X, expand=True)

# 新建（楼层数据）
class CreateNewFloor(BaseWindow):
    def drawUI(self):
        self.t.title("新建")
        self.t.geometry("500x200")
        
        self.l = tk.Label(self.t, text="新建楼层数据", bg="azure", font=self.font, width=15, height=2)
        self.l.pack(side="top", fill=tk.X)
        
        self.l2 = tk.Label(self.t, text="楼层从", bg="azure", font=self.font, height=2)
        self.l2.pack(side="left", expand=True)
        
        self.e1 = tk.Entry(self.t, font=self.font, width=10)
        self.e1.pack(side="left", expand=True)
        
        self.l3 = tk.Label(self.t, text="到", bg="azure", font=self.font, height=2)
        self.l3.pack(side="left", expand=True)
        
        self.e2 = tk.Entry(self.t, font=self.font, width=10)
        self.e2.pack(side="left", expand=True)
        
        self.b = tk.Button(self.t, text="创建地图", command=partial(self.create_floor_data, self.e1, self.e2))
        self.b.pack(side="left", expand=True)
        
    # 新建地图数据并保存    
    def create_floor_data(self, e1, e2):
        min_floor = e1.get()
        max_floor = e2.get()
        try:
            min_floor = int(min_floor)
        except ValueError:
            tkinter.messagebox.showwarning(title="警告", message="检测到非法min_floor，编辑器将使用预设数值！")
            min_floor = 0
        try:
            max_floor = int(max_floor)
        except ValueError:
            tkinter.messagebox.showwarning(title="警告", message="检测到非法max_floor，编辑器将使用预设数值！")
            max_floor = 5
        if max_floor < min_floor:
            tkinter.messagebox.showwarning(title="警告", message="你填写的min_floor比max_floor大，编辑器将自动对调两个数值！")
            min_floor, max_floor = max_floor, min_floor
        
        data = {}
        floor_num = min_floor
        for index in range(max_floor - min_floor + 1):
            data[f"MT{floor_num}"] = {}
            data[f"MT{floor_num}"]["title"] = f"魔塔 {floor_num} 层"
            data[f"MT{floor_num}"]["name"] = f"{floor_num}"
            data[f"MT{floor_num}"]["width"] = 13
            data[f"MT{floor_num}"]["height"] = 13
            data[f"MT{floor_num}"]["map"] = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                 [0, 1, 32, 0, 32, 1, 87, 1, 29, 1, 29, 1, 0],
                                 [0, 1, 1, 202, 1, 1, 0, 1, 0, 1, 0, 1, 0],
                                 [0, 1, 201, 0, 31, 1, 205, 1, 202, 1, 201, 1, 0],
                                 [0, 1, 0, 1, 0, 201, 0, 201, 0, 205, 0, 1, 0],
                                 [0, 1, 202, 1, 1, 1, 202, 1, 201, 1, 29, 1, 0],
                                 [0, 1, 0, 205, 0, 201, 81, 201, 0, 1, 1, 1, 0],
                                 [0, 1, 31, 1, 201, 1, 21, 1, 205, 1, 28, 1, 0],
                                 [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                                 [0, 1, 27, 1, 28, 1, 0, 1, 32, 0, 27, 1, 0],
                                 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
            data[f"MT{floor_num}"]["canFlyTo"] = True
            data[f"MT{floor_num}"]["canUseQuickShop"] = True
            data[f"MT{floor_num}"]["cannotViewMap"] = False
            data[f"MT{floor_num}"]["item_ratio"] = 1
            data[f"MT{floor_num}"]["firstArrive"] = None
            data[f"MT{floor_num}"]["eachArrive"] = None
            data[f"MT{floor_num}"]["events"] = None
            data[f"MT{floor_num}"]["bgm"] = None
            floor_num += 1
        
        save_to_file(data)

# 读取（楼层数据）
class LoadFloor(BaseWindow):
    def drawUI(self):
        self.t.title("加载")
        self.t.geometry("500x300")
        
        self.l = tk.Label(self.t, text="加载地图数据", bg="azure", font=self.font, width=15, height=2)
        self.l.pack(side="top", fill=tk.X)
        
        self.l2 = tk.Label(self.t, text="地图数据文件路径", bg="azure", font=self.font, height=2)
        self.l2.pack(side="left", expand=True)
        
        self.e1 = tk.Entry(self.t, font=self.font, width=30)
        self.floor_data_path = global_var.get_value("floor_data_path")
        self.e1.insert(tk.END, f"{self.floor_data_path}")
        self.e1.pack(side="left", expand=True)
        
        self.b = tk.Button(self.t, text="读取地图", command=partial(read_file, self.e1))
        self.b.pack(side="left", expand=True)

# 楼层数据编辑界面
class FloorEditor(BaseWindow):
    def drawUI(self):
        self.t.title("编辑楼层信息")
        self.t.geometry("500x300")
        self.floor_listbox = global_var.get_value("floor_listbox")
        self.floor_data = global_var.get_value("floor_data")
        
        # 获取当前选中的楼层
        self.floor_index = self.floor_listbox.get(self.floor_listbox.curselection())
        
        # 显示界面分区
        self.frame_left = tk.Frame(self.t)
        self.frame_right = tk.Frame(self.t)
        self.frame_left.pack(side="left", fill=tk.BOTH, expand=1)
        self.frame_right.pack(side="right", fill=tk.BOTH, expand=1)
        
        # 楼层属性列表
        self.l = tk.StringVar()
        self.l.set([])
        self.l = tk.Listbox(self.frame_left, listvariable=self.l, font=self.font)
        self.l.pack(side="top", fill=tk.BOTH, expand=1)
        for key in self.floor_data[self.floor_index]:
            self.l.insert("end", key)
        self.l.select_set(0)
        self.current_index = self.l.get(self.l.curselection())
        print(f"new_index: {self.current_index}")
        self.text_field = tk.Text(self.frame_right, font=self.font)

        self.text_field.insert(tk.END, json.dumps(self.floor_data[self.floor_index][self.current_index], ensure_ascii=False))
        self.text_field.pack(side="top", fill=tk.BOTH, expand=1)
        self.l.bind('<ButtonRelease-1>', self.flush_floor_data)
        
    # 刷新右侧楼层信息
    def flush_floor_data(self, *args):
        self.check_diff()
        self.current_index = self.l.get(self.l.curselection())
        print(f"new index: {self.current_index}")
        print(f"data: {self.floor_data[self.floor_index][self.current_index]}")
        self.text_field.delete("1.0",tk.END)
        self.text_field.insert(tk.END, json.dumps(self.floor_data[self.floor_index][self.current_index], ensure_ascii=False))
        
    # 检查选中数据内容变化
    def check_diff(self):
        original = json.dumps(self.floor_data[self.floor_index][self.current_index], ensure_ascii=False)
        new = self.text_field.get("1.0",'end-1c')
        print(f"original {original} new {new}")
        if original != new:
            diff = json.loads(new)
            self.floor_data[self.floor_index][self.current_index] = diff
            status_text = global_var.get_value("status_text")
            status_text.set(f"成功修改[{self.floor_index}][{self.current_index}]！")

if __name__ == "__main__":
    global_var._init()
    root = tk.Tk()
    root.title("地图数据编辑器")
    root.geometry("854x480")
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
