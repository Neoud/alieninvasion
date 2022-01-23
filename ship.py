import pygame
from settings import Settings
from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船的类"""
    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 设置飞船初始位置
        self.rect.midbottom = self.screen_rect.midbottom

        # 获取飞船配置
        self.settings = Settings()
        self.x = float(self.rect.x)

        # 设置移动标志
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """在屏幕上绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """更新飞船外接矩形的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def center_ship(self):
        """飞船居中"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
