# -*- coding:utf-8 -*-
"""
游戏主控台
"""
__author__ = "Cliff.wang"

import pygame

from settings import Settings
from fighter import Fighter
from enemy import Enemy
from supply import Supply
import controlFunc as cf
from gameStats import GameStats

def run_game():
    #获取游戏参数
    game_settings = Settings()

    #初始化游戏
    pygame.init()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("飞机大战")

    #初始化游戏控制
    gs = GameStats(game_settings, screen)

    #定义玩家
    player = Fighter(game_settings, screen, gs.img_role)

    #存储敌机
    enemies1 = pygame.sprite.Group()
    enemies_down = pygame.sprite.Group()

    #存储补给
    supplies = pygame.sprite.Group()

    #定义时钟
    clock = pygame.time.Clock()

    while True:
        # 控制游戏帧数，表示每秒循环60次
        clock.tick(60)

        if gs.bStarted and not gs.bPaused and not gs.bOver and not gs.bWin:
            #发射子弹
            player.shoot(gs)

            #生成敌机
            Enemy.discover(game_settings, gs, enemies1)

            #生成补给
            Supply.discover(game_settings, gs, supplies)

            #更新敌机并检测碰撞
            cf.update_enemies(screen, enemies1, enemies_down, player, gs.sound_gameover)

            #更新子弹并检测碰撞
            cf.update_bullets(game_settings, player, enemies1, enemies_down, supplies)

            #更新补给并检测碰撞
            cf.update_supplies(game_settings, gs, player, enemies1, enemies_down, supplies)

        #更新画面
        cf.update_screen(game_settings, gs, screen, player, enemies1, enemies_down, supplies)

        #鼠标和键盘事件处理
        cf.check_events(gs, player)


run_game()
