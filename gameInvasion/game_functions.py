# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import sys
from time import sleep
import pygame
from alien import Alien
from bullet import Bullet

def check_keydown_event(event, ai_settings, stats, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        if stats.game_active and len(bullets) < ai_settings.bullets_allowed:
            bullets.add(Bullet(ai_settings, screen, ship))
    elif event.key == pygame.K_q:
        stats.high_score_store()
        sys.exit()

def check_keyup_event(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_settings, stats, screen, play_button, score_board, ship, aliens, bullets):
    """
    响应按键和鼠标事件
    :return:
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.high_score_store()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if not stats.game_active and play_button.rect.collidepoint(mouse_x, mouse_y):
                #重置统计信息
                stats.reset_stats()
                stats.game_active = True

                #清空外星人和子弹列表
                aliens.empty()
                bullets.empty()

                #创建一群外星人，飞船居中
                create_fleet(ai_settings, screen, ship, aliens)
                ship.centerx = screen.get_rect().centerx
                ship.bottom = screen.get_rect().bottom

                #重置记分牌
                score_board.prep_score()
                score_board.prep_level()
                score_board.prep_ships()

                #隐藏光标
                pygame.mouse.set_visible(False)

        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, stats, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)

def create_fleet(ai_settings, screen, ship, aliens):
    """
    创建外星人群
    :param ai_settings:
    :param screen:
    :param aliens:
    :return:
    """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    availabel_space_x = ai_settings.screen_width - 2 * alien_width
    number_cols = int(availabel_space_x / (2 * alien_width))
    availabel_space_y = ai_settings.screen_height - 3 * alien_height - ship.rect.height
    number_rows = int(availabel_space_y / (2 * alien_height))

    #创建一群外星人
    for i in range(number_cols):
        for j in range(number_rows):
            alien = Alien(ai_settings, screen)
            alien.x = alien_width + 2 * alien_width * i
            alien.y = alien_height + 2 * alien_height * j
            alien.rect.x = alien.x
            alien.rect.y = alien.y
            aliens.add(alien)

def ship_hit(ai_settings, stats, screen, score_board, ship, aliens, bullets):
    """
    飞船坠毁处理
    :param ai_settings:
    :param stats:
    :param screen:
    :param ship:
    :param aliens:
    :param bullets:
    :return:
    """
    if stats.ships_left > 0:
        #飞船数量减1
        stats.ships_left -= 1

        #外星人及子弹清空
        aliens.empty()
        bullets.empty()

        #创建新的外星人，飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        screen_rect = screen.get_rect()
        ship.centerx = screen_rect.centerx
        ship.bottom = screen_rect.bottom

        #暂停0.5秒
        sleep(0.5)
    else:
        stats.game_active = False
        ai_settings.init_dynamic_settings()
        pygame.mouse.set_visible(True)
    score_board.prep_ships()

def update_aliens(ai_settings, stats, screen, score_board, ship, aliens, bullets):
    """
    更新外星人位置
    :param aliens:
    :return:
    """
    bEdges = False
    for alien in aliens.sprites():
        if alien.check_edges():
            bEdges = True
            break
    if bEdges:
        for alien in aliens.sprites():
            alien.rect.y += ai_settings.fleet_drop_speed
        ai_settings.fleet_direction *= -1
    aliens.update()

    #检测外星人撞到飞船
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, score_board, ship, aliens, bullets)

    #检测外星人到达屏幕底部
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, score_board, ship, aliens, bullets)
            break

def update_bullets(ai_settings, stats, screen, score_board, ship, aliens, bullets):
    """
    更新子弹
    :param bullets:
    :return:
    """
    bullets.update()
    for bullet in bullets:
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    #检查子弹是否击中了外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for alien in collisions.values():
            stats.score += ai_settings.alien_points * len(alien)
        score_board.prep_score()
        if stats.score > stats.high_score:
            stats.high_score = stats.score
    if stats.high_score > 0:
        score_board.prep_high_score()

    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ai_settings.increase_speed()
        stats.level += 1
        score_board.prep_level()

def update_screen(ai_settings, stats, screen, play_button, score_board, ship, aliens, bullets):
    """
    更新屏幕上的图像，并切换到新屏幕
    :param ai_settings:
    :param screen:
    :param ship:
    :return:
    """

    # 每次循环都重绘屏幕
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    #显示记分牌
    score_board.show_score()

    #如果游戏为非活动状态，则显示开始按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的图片可见
    pygame.display.flip()
