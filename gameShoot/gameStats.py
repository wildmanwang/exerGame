#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
游戏状态控制
"""

__author__ = 'Cliff Wang'

import pygame
import time

from button import Button

class GameStats():
    """
    资源定义
    游戏状态控制
    """
    def __init__(self, game_settings, screen):
        """
        游戏状态初始化
        :param game_settings: 全局设置
        """
        self.game_settings = game_settings

        self.img_background = pygame.image.load(r"resources/image/background.png").convert()
        self.img_gameover = pygame.image.load(r"resources/image/gameover.png")
        self.img_role = pygame.image.load(r"resources/image/shoot.png")
        #子弹
        self.img_bullet1 = self.img_role.subsurface(game_settings.bullet_rect)
        width = self.img_bullet1.get_rect().width
        height = self.img_bullet1.get_rect().height
        self.img_bullet2 = pygame.transform.smoothscale(self.img_bullet1, (width * 2, height))
        self.img_bullet3 = pygame.transform.smoothscale(self.img_bullet1, (width * 3, height))
        self.img_bullet4 = pygame.transform.smoothscale(self.img_bullet1, (width * 4, height))
        self.img_bullet5 = pygame.transform.smoothscale(self.img_bullet1, (width * 5, height))
        self.img_bullet6 = pygame.transform.smoothscale(self.img_bullet1, (width * 6, height))
        self.img_bullet7 = pygame.transform.smoothscale(self.img_bullet1, (width * 7, height))
        self.img_bullet8 = pygame.transform.smoothscale(self.img_bullet1, (width * 8, height))
        self.img_bullet9 = pygame.transform.smoothscale(self.img_bullet1, (width * 9, height))
        self.img_bullet10 = pygame.transform.smoothscale(self.img_bullet1, (width * 10, height))
        #战机数量标识：把玩家战机图片长宽分别缩小1/2
        #self.img_icon = self.img_role.subsurface(game_settings.player_rect[0]).convert_alpha()
        #战机数量标识：把琪琪照片长宽分别缩小1/8
        self.img_icon = pygame.image.load(r"resources/image/Maggie_icon.png")
        self.img_icon = pygame.transform.smoothscale(self.img_icon, (int(self.img_icon.get_rect().width / 8), int(self.img_icon.get_rect().height / 8)))
        #补给
        self.img_supply = pygame.image.load(r"resources/image/Maggie_supply.png")
        self.img_supply = pygame.transform.smoothscale(self.img_supply, (int(self.img_supply.get_rect().width / 6), int(self.img_supply.get_rect().height / 6)))
        self.supply_time = time.time()

        pygame.mixer.music.load(r"resources/sound/game_music.wav")
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.25)

        self.sound_bullet = pygame.mixer.Sound(r"resources/sound/bullet.wav")
        self.sound_bullet.set_volume(0.3)
        self.sound_enemy1_down = pygame.mixer.Sound(r"resources/sound/enemy1_down.wav")
        self.sound_enemy1_down.set_volume(0.3)
        self.sound_gameover = pygame.mixer.Sound(r"resources/sound/game_over.wav")
        self.sound_gameover.set_volume(0.3)

        self.btn_play = Button(screen, "Play", 0)
        self.btn_continue = Button(screen, "Continue", 0)
        self.btn_exit = Button(screen, "Exit", 1)

        self.game_reset()

    def game_play(self):
        """
        开始游戏
        :return: None
        """
        self.game_reset()
        self.bStarted = True

    def game_pause(self):
        """
        暂停/继续游戏
        :return: None
        """
        self.bPaused = not self.bPaused

    def game_collide(self):
        """
        战机被击毁
        :return:
        """
        if self.player_times > 0:
            self.player_times -= 1
            self.frequency_shoot = 0
            self.frequency_enemy = 0
            self.player_down_index = 16
            time.sleep(0.5)
        else:
            self.bOver = True

    def game_reset(self):
        """
        游戏重置
        :return:
        """
        self.player_times = self.game_settings.player_times - 1
        self.score = 0                      #当前记分
        self.frequency_shoot = 0
        self.frequency_enemy = 0
        self.player_down_index = 16
        self.supply_time = time.time()

        self.bStarted = False               #游戏是否开始了
        self.bPaused = False                #游戏是否暂停了
        self.bOver = False                  #游戏是否结束了
        self.bWin = False                   #游戏是否赢了
