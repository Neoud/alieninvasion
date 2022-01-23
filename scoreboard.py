import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化现实得分涉及的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.status= ai_game.status

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分渲染为一幅渲染的图像"""
        rounded_score = round(self.status.score, -1)
        score_str = "{:,}".format(rounded_score)
        score_str = str(self.status.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # 设置图像位置
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """将最高得分渲染为图像"""
        high_score = round(self.status.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # 将最高分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.score_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """检查是否诞生了新的最高分"""
        if self.status.score > self.status.high_score:
            self.status.high_score = self.status.score
            self.prep_high_score()

    def prep_level(self):
        """将等级转换为渲染的图像"""
        level_str = str(self.status.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # 设置等级位置
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还剩下多少飞船"""
        self.ships = Group()
        for ship_number in range(self.status.ships_left):
            ship = Ship(self.ai_game)
            ship.image = pygame.transform.scale(ship.image, self.settings.alien_size)
            ship.rect = ship.image.get_rect()
            ship.rect.x = self.screen_rect.width - (10 + ship_number * ship.rect.width)
            ship.rect.y = self.screen_rect.height - (ship.rect.height + 10)
            self.ships.add(ship)
