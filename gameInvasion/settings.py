# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

class Settings():
    """
    存储参数设置
    """

    def __init__(self):
        """
        初始化游戏的设置
        """

        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #飞船设置
        self.ship_limit = 3

        #子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (221, 67, 67)
        self.bullets_allowed = 5

        #外星人设置
        self.fleet_drop_speed = 15
        self.fleet_direction = 1        #{1:"向右边", -1:"向左边"}

        #难度比例
        self.speedup_scale = 1.1
        self.score_scale = 1.2

        #动态参数初始化
        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        self.ship_speed_factor = 2.5
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 1
        self.alien_points = 10

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
