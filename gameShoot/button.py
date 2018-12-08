# -*- coding:utf-8 -*-
"""
按钮类
"""
__author__ = "Cliff.wang"

import pygame.font

class Button():
    """
    按钮类
    """
    def __init__(self, screen, msg, pos):
        """
        创建按钮
        :param screen: 载体surface
        :param msg: 按钮文字
        :param pos: 第几个按钮，用于排列
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #设置按钮属性
        self.width, self.height = 200, 50
        self.button_color = (167, 167, 167)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #创建按钮rect并居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.top += 65 * pos + 50

        #创建文字标签
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """
        显示按钮
        :return:
        """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
