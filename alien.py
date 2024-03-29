import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个alien的类"""
    def __init__(self, ai_game):
        """初始化外星人并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图像并获取其外接矩形
        self.image = pygame.image.load('images/alien1.bmp')
        self.image = pygame.transform.scale(self.image, self.settings.alien_size)
        self.rect = self.image.get_rect()

        # 设置初始位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精准水平位置
        self.x = float(self.rect.x)

    def update(self):
        """向右或向左移动外星人"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人位于屏幕边缘则返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.x + self.rect.width >= screen_rect.right or self.rect.left <= 0:
            return True
