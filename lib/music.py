import pygame
import os
from sysconf import *
from lib import CurrentMap, WriteLog

class MusicWrapper():
    def __init__(self):
        self.current_bgm = None
        # pygame需要初始化音乐模块后才能进行播放
        pygame.mixer.init()
        # 在这里加载全部音乐
        self.play_BGM("bgm.mp3")
        # some_sound = pygame.mixer.Sound(path.join(snd_dir, "some.wav"))
        # 背景音乐的音量（0-1）
        pygame.mixer.music.set_volume(0.5)
        # 让背景音乐循环播放
        pygame.mixer.music.play(loops=-1)
        self.load_SE()
        WriteLog.debug(__name__, "SE初始化完成！")

    # 播放BGM
    def play_BGM(self, BGM):
        if BGM != self.current_bgm:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.unload()
            try:
                pygame.mixer.music.load(path.join(bgm_dir, BGM))
                pygame.mixer.music.play(loops=-1)
                self.current_bgm = BGM
                WriteLog.debug(__name__, f"播放BGM：{BGM}！")
            except:
                WriteLog.debug(__name__, f"播放BGM失败：{BGM}！")
        else:
            WriteLog.debug(__name__, f"当前正在播放BGM：{BGM}，无需切换！")

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
            WriteLog.error(__name__, "SE加载失败，请检查目录下是否混入其它文件")

    # 检查BGM文件夹下是否有指定文件
    def check_BGM(self, BGM):
        temp_list = self.scan_dir(bgm_dir)
        if BGM in temp_list:
            return True
        else:
            return False

    # 播放指定的SE
    def play_SE(self, SE):
        try:
            self.SE_dict[SE].play()
            WriteLog.debug(__name__, f"播放SE：{SE}！")
        except:
            if ".mp3" in SE:
                original_SE = SE
                SE = SE.rstrip(".mp3")
                SE = SE + ".ogg"
            try:
                self.SE_dict[SE].play()
                WriteLog.info(__name__, f"SE自动修正：{original_SE} -> {SE}")
            except:
                WriteLog.error(__name__, "SE播放失败！")
    
    # 切换楼层时使用
    def change_BGM(self, new_floor):
        new_id = CurrentMap.get_floor_id(new_floor)
        try:
            new_bgm = self.MAP_DATABASE[new_id]["bgm"]
        except:
            new_bgm = None
        if new_bgm is not None and new_bgm != self.current_bgm:
            self.play_BGM(new_bgm)
        else:
            WriteLog.debug(__name__, f"无需切换当前BGM：{self.current_bgm}！")

    # 重置音效
    def reset(self):
        self.play_BGM("bgm.mp3")
