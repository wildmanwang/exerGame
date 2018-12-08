#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
游戏控制逻辑
"""

__author__ = 'Cliff Wang'

import pygame
import time


def check_events(game_stats, player):
    """
    响应键盘和鼠标事件
    :return:
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #响应退出事件
            pygame.quit()
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if not game_stats.bStarted or game_stats.bOver:
                #游戏未开始状态下或已结束
                if game_stats.btn_play.rect.collidepoint(mouse_x, mouse_y):
                    game_stats.game_play()
                    player.moveReset()
                elif game_stats.btn_exit.rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    exit()
            elif game_stats.bPaused:
                #游戏暂停状态下
                if game_stats.btn_continue.rect.collidepoint(mouse_x, mouse_y):
                    game_stats.game_pause()
                elif game_stats.btn_exit.rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    exit()

    #监听键盘事件
    if not game_stats.bWin or game_stats.bWin and game_stats.bOver:
        key_pressed = pygame.key.get_pressed()
        if game_stats.bStarted and not game_stats.bPaused and not game_stats.bOver and not player.is_hit:
            if key_pressed[pygame.K_UP]:
                player.moveUp()
            if key_pressed[pygame.K_DOWN]:
                player.moveDown()
            if key_pressed[pygame.K_LEFT]:
                player.moveLeft()
            if key_pressed[pygame.K_RIGHT]:
                player.moveRight()
        if key_pressed[pygame.K_SPACE]:
            #响应暂停操作
            if not game_stats.bStarted or game_stats.bOver:
                game_stats.game_play()
                player.moveReset()
            elif game_stats.bStarted and not game_stats.bOver:
                game_stats.game_pause()
            time.sleep(0.2)


def update_enemies(screen, enemies, enemies_down, player, sound):
    """
    更新敌机
    :return:
    """
    #敌机移动
    for enemy in enemies:
        enemy.move()
        if enemy.rect.top > screen.get_rect().height:
            enemies.remove(enemy)

    #检测敌机是否撞到玩家
    collides = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask)
    if len(collides) > 0:
        player.is_hit = True
        for enemy in collides:
            enemies_down.add(enemy)
            sound.play()


def update_bullets(game_settings, player, enemies, enemies_down, supplies):
    """
    更新子弹
    :return:
    """
    #子弹移动
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.top < 0:
            player.bullets.remove(bullet)

    #检测是否击中敌机
    collides = pygame.sprite.groupcollide(enemies, player.bullets, True, True)
    for enemy in collides:
        enemies_down.add(enemy)

    #检测是否击中补给
    for supply in supplies:
        if supply.rect.bottom > game_settings.supply_protect:
            collides = pygame.sprite.spritecollide(supply, player.bullets, True, pygame.sprite.collide_mask)
            if len(collides) > 0:
                supplies.remove(supply)
                if player.bullet_width > 1:
                    player.bullet_width -= 1


def update_supplies(game_settings, game_stats, player, enemies, enemies_down, supplies):
    """
    更新补给
    :param screen:
    :param supplies:
    :return:
    """
    #碰撞检测
    collides = pygame.sprite.spritecollide(player, supplies, True, pygame.sprite.collide_mask)
    if len(collides) > 0:
        if player.bullet_width < game_settings.supply_win:
            player.bullet_width += 1
        if player.bullet_width >= game_settings.supply_win:
            #win the game
            game_stats.bWin = True
            player.moveReset()
            player.bullet_width = game_settings.supply_win
            player.bullets.empty()
            for enemy in enemies:
                enemies.remove(enemy)
                enemies_down.add(enemy)

    #补给移动
    for supply in supplies:
        supply.move()


def update_screen(game_settings, game_stats, screen, player, enemies, enemies_down, supplies):
    """
    更新屏幕
    :return:
    """
    #绘制背景
    screen.fill(0)
    screen.blit(game_stats.img_background, (0, 0))

    #绘制玩家
    if not player.is_hit:
        player.blitme()
        player.img_index = game_stats.frequency_shoot // 8
    else:
        player.img_index = game_stats.player_down_index // 8
        player.blitme()
        if game_stats.player_down_index < 47:
            game_stats.player_down_index += 1
        else:
            enemies.empty()
            supplies.empty()
            game_stats.supply_time = time.time()
            game_stats.game_collide()
            if not game_stats.bOver:
                player.moveReset()
    if game_stats.bWin:
        game_stats.frequency_shoot += 1
        if game_stats.frequency_shoot >= 15:
            game_stats.frequency_shoot = 0
        if not player.moveWin():
            game_stats.bOver = True

    #绘制击毁动画
    for enemy in enemies_down:
        if enemy.down_index == 0:
            game_stats.sound_enemy1_down.play()
        if enemy.down_index > 7:
            enemies_down.remove(enemy)
            game_stats.score += 10
            continue
        screen.blit(enemy.down_imgs[enemy.down_index // 2], enemy.rect)
        enemy.down_index += 1

    #绘制子弹、敌机和补给
    player.bullets.draw(screen)
    enemies.draw(screen)
    supplies.draw(screen)

    #绘制得分
    if not game_stats.bStarted or not game_stats.bOver and not game_stats.bWin:
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render("{score}  {bullet_width}/{supply_win}".format(score=game_stats.score, bullet_width=player.bullet_width, supply_win=game_settings.supply_win), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)
    # 游戏结束
    if game_stats.bOver and not game_stats.bWin:
        screen.blit(game_stats.img_gameover, (0, 0))
    if game_stats.bOver or game_stats.bWin:
        score_font = pygame.font.Font(None, 48)
        if game_stats.bWin:
            color = (167, 167, 167)
        else:
            color = (255, 0, 0)
        score_text = score_font.render("Score:{score}  {bullet_width}/{supply_win}".format(score=game_stats.score, bullet_width=player.bullet_width, supply_win=game_settings.supply_win), True, color)
        text_rect = score_text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        if game_stats.bWin:
            text_rect.centery = screen.get_rect().centery - 80
        else:
            text_rect.centery = screen.get_rect().centery - 150
        screen.blit(score_text, text_rect)
    if game_stats.bWin:
        score_font = pygame.font.Font(None, 60)
        score_text = score_font.render("You win!", True, (221, 67, 67))
        text_rect = score_text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery - 20
        screen.blit(score_text, text_rect)

    #显示剩余战机数量
    icon_rect = game_stats.img_icon.get_rect()
    icon_rect.top = 10
    for i in range(game_stats.player_times):
        icon_rect.right = screen.get_rect().width - 10 - i * (10 + icon_rect.width)
        screen.blit(game_stats.img_icon, icon_rect)

    #显示按钮
    if not game_stats.bStarted:
        game_stats.btn_play.draw_button()
        game_stats.btn_exit.draw_button()
    elif game_stats.bStarted and game_stats.bPaused:
        game_stats.btn_continue.draw_button()
        game_stats.btn_exit.draw_button()
    elif game_stats.bOver:
        game_stats.btn_play.draw_button()
        game_stats.btn_exit.draw_button()

    #更新屏幕
    pygame.display.update()
