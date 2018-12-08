# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """
    外星人
    """

    def __init__(self, ai_settings, screen):
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        #加载外星人图像
        self.image = pygame.image.load("images/alien.bmp").convert()
        self.rect = self.image.get_rect()

        #定位外星人在左下角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #存储外星人准确位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """
        检测外星人是否位于屏幕边缘
        :return:
        """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.left <= 0:
            return True

    def update(self):
        """
        更新外星人位置
        :return:
        """
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """
        在指定位置绘制外星人
        :return:
        """
        self.screen.blit(self.image, self.rect)
