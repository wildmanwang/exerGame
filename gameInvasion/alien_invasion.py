# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #初始化游戏，创建主窗口
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("外星人入侵")

    #创建统计实例
    stats = GameStats(ai_settings)

    #创建开始按钮
    play_button = Button(ai_settings, screen, "Play")

    #创建记分牌
    score_board = Scoreboard(ai_settings, screen, stats)

    #创建一艘飞船
    ship = Ship(ai_settings, screen)
    #创建子弹编组
    bullets = Group()
    #创建外星人编组
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings, stats, screen, play_button, score_board, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_aliens(ai_settings, stats, screen, score_board, ship, aliens, bullets)
            gf.update_bullets(ai_settings, stats, screen, score_board, ship, aliens, bullets)
        gf.update_screen(ai_settings, stats, screen, play_button, score_board, ship, aliens, bullets)

run_game()
