# --coding=utf-8

from src.game import *

class Game(GamePage):
    def __init__(self):
        mixer.init()
        # 音乐
        mixer.music.load("media\\background.ogg")
        mixer.music.set_volume(CONFIG["music_vol"])
        mixer.music.play(-1)
        # 音效
        self.f_initSounds()
        # 开始游戏
        self.page_mainMenu()

if __name__ == '__main__':
    Game()
