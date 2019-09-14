import json5
import json
import os

class MapConvert():
    def __init__(self):
        # self.path 就是H5魔塔地图的所在路径，请自行调整
        self.path = "/中秋2019：桂魄/project/floors/"
        # self.output_dir_name 是输出文件的目录，可以自行设定
        self.output_dir_name =  "convert"
        self.save_path = os.path.join(os.getcwd(), self.output_dir_name)
        self.item = ""
        self.check_output_dir()
        self.map_list = self.scan_dir()

    def check_output_dir(self):
        if not os.path.exists(self.output_dir_name):
            os.makedirs(self.output_dir_name)

    def convert(self):
        for item in self.map_list:
            self.item = item
            self.parse()
            self.save()

    def parse(self):
        with open(os.path.join(self.path, self.item)) as f:
            next(f)
            self.map_data = json5.load(f)

    def save(self):
        file_name = self.item.split(".")[0] + ".json"
        with open(os.path.join(self.save_path, file_name), "w") as f:
            json.dump(self.map_data, f)
        print(f"成功将{self.item}转换成{file_name}！")


    def scan_dir(self):
        return os.listdir(self.path)


converter = MapConvert()
converter.convert()