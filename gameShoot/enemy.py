#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
敌机类
"""

__author__ = 'Cliff Wang'

import pygame
import random

class Enemy(pygame.sprite.Sprite):
    """
    敌机类
    """
    def __init__(self, game_settings, rs_img, enemy_no):
        pygame.sprite.Sprite.__init__(self)
        # 敌机型号，支持0：小飞机
        self.no = enemy_no
        self.rect = pygame.Rect(game_settings.enemy1_rect[0])
        self.image = rs_img.subsurface(self.rect)
        self.rect.bottom = 0
        self.rect.left = random.randint(0, game_settings.screen_width - self.rect.width)
        self.speed = game_settings.enemy_speed
        self.down_imgs = []
        for i in range(len(game_settings.enemy1_rect)):
            if i > 0:
                self.down_imgs.append(rs_img.subsurface(game_settings.enemy1_rect[i]))
        self.down_index = 0
        #用于非透明碰撞检测
        self.mask = pygame.mask.from_surface(self.image)

    @staticmethod
    def discover(game_settings, game_stats, enemies):
        """
        发现敌机来了
        :param game_settings: 全局参数
        :param game_stats: 全局状态
        :param enemies: 敌人Group
        :return: None
        """
        if game_stats.frequency_enemy % 50 == 0:
            enemies.add(Enemy(game_settings, game_stats.img_role, 0))
        game_stats.frequency_enemy += 1
        if game_stats.frequency_enemy >= 100:
            game_stats.frequency_enemy = 0

    def move(self):
        """
        敌机移动
        :return: None
        """
        self.rect.top += self.speed
