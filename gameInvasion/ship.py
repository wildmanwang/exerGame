# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """
    飞船
    """

    def __init__(self, ai_settings, screen):
        """
        初始化飞船
        :param screen:飞船绘制到什么地方
        """
        super().__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        #加载飞船图像并获取外接矩形
        self.image = pygame.image.load("images/ship.bmp").convert()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #将每艘飞船放到屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #在飞船的属性center中存储小数
        self.centerx = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        #移动标识
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """
        根据标识移动飞船位置
        :return:
        """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.bottom -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ai_settings.ship_speed_factor
        self.rect.centerx = self.centerx
        self.rect.bottom = self.bottom

    def blitme(self):
        """
        在指定位置绘制飞船
        :return:
        """
        self.screen.blit(self.image, self.rect)
