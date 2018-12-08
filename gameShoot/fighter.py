# -*- coding:utf-8 -*-
"""
玩家定义
"""
__author__ = "Cliff.wang"

import pygame


class Bullet(pygame.sprite.Sprite):
    """
    玩家子弹
    """
    def __init__(self, game_settings, game_stats, init_pos, bullet_width):
        """
        创建子弹
        :param game_settings: 全局参数
        :param rs_img: 全局资源
        :param init_pos: 发射位置
        """
        pygame.sprite.Sprite.__init__(self)
        if bullet_width == 1:
            self.image = game_stats.img_bullet1
        elif bullet_width == 2:
            self.image = game_stats.img_bullet2
        elif bullet_width == 3:
            self.image = game_stats.img_bullet3
        elif bullet_width == 4:
            self.image = game_stats.img_bullet4
        elif bullet_width == 5:
            self.image = game_stats.img_bullet5
        elif bullet_width == 6:
            self.image = game_stats.img_bullet6
        elif bullet_width == 7:
            self.image = game_stats.img_bullet7
        elif bullet_width == 8:
            self.image = game_stats.img_bullet8
        elif bullet_width == 9:
            self.image = game_stats.img_bullet9
        elif bullet_width >= 10:
            self.image = game_stats.img_bullet10
        else:
            self.image = game_stats.img_bullet1
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = game_settings.bullet_speed

    def move(self):
        """
        移动子弹
        :return: None
        """
        self.rect.top -= self.speed


class Fighter(pygame.sprite.Sprite):
    """
    玩家战机
    """
    def __init__(self, game_settings, screen, rs_img):
        """
        创建战机
        :param game_settings: 全局参数
        :param screen: 游戏界面surface
        :param rs_img: 全局资源
        """
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.game_settings = game_settings
        self.rs_img = rs_img
        self.image = []
        for i in range(len(self.game_settings.player_rect)):
            self.image.append(rs_img.subsurface(self.game_settings.player_rect[i]).convert_alpha())
        self.img_index = 0
        self.rect = pygame.Rect(self.game_settings.player_rect[0])
        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.top = self.game_settings.screen_height - 2 * self.rect.height
        self.speed = self.game_settings.player_speed
        self.bullet_width = 1
        self.bullets = pygame.sprite.Group()
        self.is_hit = False
        # 用于非透明碰撞检测
        self.mask = pygame.mask.from_surface(self.image[0])

    def blitme(self):
        """
        绘制角色
        :return:
        """
        self.screen.blit(self.image[self.img_index], self.rect)

    def shoot(self, game_stats):
        """
        射击
        :param game_stats: 全局状态
        :return: None
        """
        if not self.is_hit:
            if game_stats.frequency_shoot % 15 == 0:
                game_stats.sound_bullet.play()
                bullet = Bullet(self.game_settings, game_stats, self.rect.midtop, self.bullet_width)
                self.bullets.add(bullet)
            game_stats.frequency_shoot += 1
            if game_stats.frequency_shoot >= 15:
                game_stats.frequency_shoot = 0

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.bottom < self.game_settings.screen_height:
            self.rect.bottom += self.speed

    def moveLeft(self):
        if self.rect.centerx > 0:
            self.rect.centerx -= self.speed

    def moveRight(self):
        if self.rect.centerx < self.game_settings.screen_width:
            self.rect.centerx += self.speed

    def moveReset(self):
        """
        被击毁后新重置新战机
        :return:
        """
        self.img_index = 0
        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.top = self.game_settings.screen_height - 2 * self.rect.height
        self.bullet_width = 1
        self.is_hit = False

    def moveWin(self):
        """
        胜利画面
        :return:
        """
        if self.rect.top > 10:
            self.rect.top -= 1
            return True
        else:
            return False
