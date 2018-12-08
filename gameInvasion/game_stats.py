# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

class GameStats():
    """
    跟踪游戏统计信息
    """

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.game_active = False
        self.high_score_load()
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def high_score_store(self):
        with open("data\\score.txt", "w", encoding="utf-8") as f:
            f.write(str(self.high_score))

    def high_score_load(self):
        try:
            with open("data\\score.txt", "r", encoding="utf-8") as f:
                score_str = str(f.read())
                if score_str.isdigit():
                    self.high_score = int(score_str)
                else:
                    self.high_score = 0
        except FileNotFoundError:
            self.high_score = 0

