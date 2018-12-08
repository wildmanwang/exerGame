# -*- coding:utf-8 -*-
"""
游戏参数及资源定义
"""
__author__ = "Cliff.wang"

class Settings():
    """
    存储游戏参数
    """

    def __init__(self):
        """
        初始化游戏参数
        """

        #屏幕参数
        self.screen_width = 480
        self.screen_height = 800

        #玩家参数
        self.player_times = 3
        self.player_rect = [
            (0, 99, 102, 126),
            (165, 360, 102, 126),
            (165, 234, 102, 126),
            (330, 624, 102, 126),
            (330, 498, 102, 126),
            (430, 624, 102, 126)
        ]
        self.player_speed = 8

        #子弹参数
        self.bullet_rect = (1004, 987, 9, 21)
        self.bullet_speed = 10

        #补给参数
        self.supply_speed = 1
        self.supply_interval = 10           #补给间隔：单位秒
        self.supply_win = 10                #最大胜利数
        self.supply_protect = 50            #补给在多大位置受到保护，难度：150/100/50

        #敌机参数
        self.enemy1_rect = [
            (534, 612, 57, 43),
            (267, 347, 57, 43),
            (873, 697, 57, 43),
            (267, 296, 57, 43),
            (930, 697, 57, 43)
        ]
        self.enemy_speed = 3                #难度：2/3/3
