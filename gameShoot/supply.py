# -*- coding:utf-8 -*-
"""
补给
"""
__author__ = "Cliff.wang"

import pygame
import random
import time

class Supply(pygame.sprite.Sprite):
    """
    补给类
    """
    def __init__(self, game_settings, game_stats):
        pygame.sprite.Sprite.__init__(self)
        self.image = game_stats.img_supply
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, game_settings.screen_width - self.rect.width)
        self.rect.bottom = 0
        self.speed = game_settings.supply_speed
        # 用于非透明碰撞检测
        self.mask = pygame.mask.from_surface(self.image)

    @staticmethod
    def discover(game_settings, game_stats, supplies):
        curTime = time.time()
        if curTime - game_stats.supply_time > game_settings.supply_interval:
            supply = Supply(game_settings, game_stats)
            supplies.add(supply)
            game_stats.supply_time = curTime

    def move(self):
        """
        移动
        :return:
        """
        self.rect.top += self.speed
