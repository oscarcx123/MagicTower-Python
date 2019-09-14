import pygame
import os
from sysconf import *

class MusicWrapper():
    def __init__(self):
        # pygame需要初始化音乐模块后才能进行播放
        pygame.mixer.init()
        # 在这里加载全部音乐
        pygame.mixer.music.load(path.join(bgm_dir, "xingxingdiandeng.ogg"))
        # some_sound = pygame.mixer.Sound(path.join(snd_dir, "some.wav"))
        # 背景音乐的音量（0-1）
        pygame.mixer.music.set_volume(0.5)
        # 让背景音乐循环播放
        pygame.mixer.music.play(loops=-1)
        self.load_SE()
        print("[DEBUG]SE初始化完成！")


    # 遍历file_path下所有文件，返回list
    def scan_dir(self, file_path):
        return os.listdir(file_path)

    # 加载所有SE文件夹下的音效
    def load_SE(self):
        temp_list = self.scan_dir(se_dir)
        self.SE_dict = {}
        try:
            for item in temp_list:
                self.SE_dict[item] = pygame.mixer.Sound(path.join(se_dir, item))
        except:
            print("SE加载失败，请检查目录下是否混入其它文件")

    # 播放指定的SE
    def play_SE(self, SE):
        try:
            self.SE_dict[SE].play()
        except:
            print("SE播放失败！")
        
    

