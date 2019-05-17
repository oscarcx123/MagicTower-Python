import tkinter as tk
import tkinter.messagebox
from functools import partial
import os
import json

class MainWindow(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.font = ("Arial",12)
        # 地图数据初始化
        self.floor_data = None
        # “正在编辑”状态（是否开启楼层数据编辑窗口，用于防止窗口多开）
        self.editing_floor_data = False
        
        # 菜单栏
        # menubar
        self.menubar = tk.Menu(self)

        # menubar > filemenu
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="文件", menu=self.filemenu)
        self.filemenu.add_command(label="新建", command=self.new_ui)
        self.filemenu.add_command(label="加载", command=self.load_ui)
        self.filemenu.add_command(label="保存", command=partial(self.save_to_file, self.floor_data))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="退出", command=self.quit)
        
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
        
        # 右侧地图显示
        self.map_area = tk.Text(self.frame_right, font=self.font)
        self.map_area.insert(tk.END, "TODO: 这里用来显示地图")
        self.map_area.pack(side="top", fill=tk.BOTH, expand=1)
        
        self.floor_listbox.bind('<Double-Button-1>', self.edit_floor_data_ui)
        
        # 生成默认地图数据文件路径
        self.floor_data_path = os.path.abspath(os.path.join(os.getcwd(), "..", "project", "floor_data.json"))
        
        # 默认禁用编辑，成功读取地图数据文件后会自动解禁
        self.disable_edit()
        
        # 自动尝试在启动时读取地图数据文件
        self.read_file()
        
    # 创建空白窗口函数，并不实际使用，只是作为模板方便编写其它窗口
    def create_window(self):
        t = tk.Toplevel(self)
        t.title(f"Window")
        l = tk.Label(t, text=f"This is a new window")
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
        
    # Place Holder函数，相当于pass    
    def do_job(self, *args):
        print(*args)
        print("Success!")
        
    # 启用编辑功能（加载地图文件成功）
    def enable_edit(self):
        self.filemenu.entryconfig("保存", state="normal")
    
    # 禁用编辑功能（加载地图文件失败）
    def disable_edit(self):
        self.filemenu.entryconfig("保存", state="disabled")
    
    # UI - 文件 > 新建
    def new_ui(self):
        window = tk.Toplevel(self)
        window.title("新建")
        window.geometry("500x200")
        
        l = tk.Label(window, text="新建地图数据", bg="azure", font=self.font, width=15, height=2)
        l.pack(side="top", fill=tk.X)
        
        l2 = tk.Label(window, text="楼层从", bg="azure", font=self.font, height=2)
        l2.pack(side="left", expand=True)
        
        e1 = tk.Entry(window, font=self.font, width=10)
        e1.pack(side="left", expand=True)
        
        l3 = tk.Label(window, text="到", bg="azure", font=self.font, height=2)
        l3.pack(side="left", expand=True)
        
        e2 = tk.Entry(window, font=self.font, width=10)
        e2.pack(side="left", expand=True)
        
        b = tk.Button(window, text="创建地图", command=partial(self.create_floor_data, e1, e2))
        b.pack(side="left", expand=True)
    
    # UI - 文件 > 加载
    def load_ui(self):
        window = tk.Toplevel(self)
        window.title("加载")
        window.geometry("500x300")
        
        l = tk.Label(window, text="加载地图数据", bg="azure", font=self.font, width=15, height=2)
        l.pack(side="top", fill=tk.X)
        
        l2 = tk.Label(window, text="地图数据文件路径", bg="azure", font=self.font, height=2)
        l2.pack(side="left", expand=True)
        
        e1 = tk.Entry(window, font=self.font, width=30)
        e1.insert(tk.END, f"{self.floor_data_path}")
        e1.pack(side="left", expand=True)
        
        b = tk.Button(window, text="读取地图", command=partial(self.read_file, e1))
        b.pack(side="left", expand=True)
    
    # UI - 帮助 > 关于    
    def about_ui(self):
        window = tk.Toplevel(self)
        window.title("关于")
        window.geometry("500x300")
        
        l = tk.Label(window, text="Python魔塔地图数据编辑器", bg="azure", font=self.font, width=15, height=2)
        l.pack(side="top", fill=tk.X)
        
        l2 = tk.Label(window, text="开发者：Azure", font=self.font, width=15, height=2)
        l2.pack(side="top", fill=tk.X, expand=True)
    
    # 新建地图数据并保存    
    def create_floor_data(self, e1, e2):
        min_floor = e1.get()
        max_floor = e2.get()
        print(min_floor)
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
        self.save_to_file(data)
    
    # UI - 编辑楼层信息    
    def edit_floor_data_ui(self, *args):
        self.editing_floor_data = True
        window = tk.Toplevel(self)
        window.title("编辑楼层信息")
        window.geometry("500x300")
        
        # 获取当前选中的楼层
        floor_index = self.floor_listbox.get(self.floor_listbox.curselection())
        
        # 显示界面分区
        frame_left = tk.Frame(window)
        frame_right = tk.Frame(window)
        frame_left.pack(side="left", fill=tk.BOTH, expand=1)
        frame_right.pack(side="right", fill=tk.BOTH, expand=1)
        
        # 楼层属性列表
        l = tk.StringVar()
        l.set([])
        l = tk.Listbox(frame_left, listvariable=l, font=self.font)
        l.pack(side="top", fill=tk.BOTH, expand=1)
        for key in self.floor_data[floor_index]:
            l.insert("end", key)
        l.select_set(0)
        current_index = l.get(l.curselection())
        l.event_generate("<<ListboxSelect>>")
        print(l.get(l.curselection()))
        text_field = tk.Text(frame_right, font=self.font)

        text_field.insert(tk.END, self.floor_data[floor_index][current_index])
        text_field.pack(side="top", fill=tk.BOTH, expand=1)
        l.bind('<ButtonRelease-1>', self.flush_floor_data)
        self.floor_index = floor_index
        self.text_field = text_field
        self.curl = l
        
    # 刷新右侧楼层信息
    def flush_floor_data(self, *args):
        index = self.curl.get(self.curl.curselection())
        self.text_field.delete("1.0",tk.END)
        self.text_field.insert(tk.END, self.floor_data[self.floor_index][index])
    
    # 写入floor_data.json文件
    def save_to_file(self, data):
        with open((self.floor_data_path), "w") as f:
            json.dump(data, f)
        self.status_text.set(f"成功保存到{self.floor_data_path}！")
    
    # 读取floor_data.json文件
    def read_file(self, e1=None):
        if e1 is None:
            path = self.floor_data_path
        else:
            path = e1.get()
        try:
            with open(path) as f:
                self.floor_data = json.load(f)
            print(self.floor_data) # 查看读取到的地图数据
            self.enable_edit()
            self.flush_floor_list()
            self.status_text.set(f"成功读取{path}！")
        except json.decoder.JSONDecodeError:
            self.status_text.set(f"读取失败，{path}文件为空或者格式不是JSON！")
        except FileNotFoundError:
            self.status_text.set(f"读取失败，{path}文件不存在！")
        except TypeError:
            self.status_text.set(f"读取失败，{path} not iterable！")
        except:
            self.status_text.set(f"读取失败，未知错误！")

    # 刷新左侧楼层列表
    def flush_floor_list(self):
        self.floor_listbox.delete(0,tk.END)
        for key in self.floor_data:
            self.floor_listbox.insert("end", key)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("地图数据编辑器")
    root.geometry("854x480")
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
