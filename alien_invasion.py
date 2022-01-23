import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_status import GameStatus
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.status = GameStatus(self)
        self.scoreboard = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # 创建按钮
        self.play_button = Button(self, "Play")
        print(self.screen.get_rect().width)
    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监视键盘和鼠标的事件
            self._check_events()
            # 游戏处于运行状态
            if self.status.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            # 每次循环重新绘制屏幕
            self._update_screen()

    def _check_events(self):
        """响应键盘和鼠标的事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """点击Play开始玩游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.status.game_active:
            # 重置游戏统计信息
            self.settings.initialize_dynamic_settings()
            self.status.reset_status()
            self.status.game_active = True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()

            # 清空外星人和子弹
            self.bullets.empty()
            self.aliens.empty()

            # 创建新的外星人和飞船，飞船居中
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _update_bullets(self):
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # 删除相互碰撞的子弹和外星人
        self._check_bullet_alien_collisions()
        # 外星人全部消灭后的处理逻辑
        self._check_empty_aliens()

    def _check_bullet_alien_collisions(self):
        """处理子弹和外星人碰撞逻辑"""
        collections = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collections:
            for alien in collections.values():
                self.status.score += self.settings.alien_points
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

    def _check_empty_aliens(self):
        """消除所有外星人后重新生成外星人"""
        if not self.aliens:
            # 删除现有的子弹并创建一群外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提高等级
            self.status.level += 1
            self.scoreboard.prep_level()

    def _update_aliens(self):
        """更新外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 检测是否有外星人到达屏幕底端3
        self._check_aliens_bottom()

    def _create_fleet(self):
        """创建外星人群"""
        alien_width, alien_height = self.settings.alien_size
        # 设置一行可以放置的外星人数量
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # 设置可以放置多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # 创建一个外星人并设置其初始位置，然后加入当前行
        alien = Alien(self)
        alien_width, alien_height = self.settings.alien_size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """处理外星的人到达边缘时的逻辑"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """下移所有外星人并改变左右的移动方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        # 绘制飞船
        self.ship.blitme()
        # 绘制子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 绘制外星人
        self.aliens.draw(self.screen)
        # 绘制计分板
        self.scoreboard.show_score()
        # 如果游戏暂停，绘制按钮
        if not self.status.game_active:
            self.play_button.draw_button()
        # 让新绘制的屏幕可见
        pygame.display.flip()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # 向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 向左移动飞船
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullet_number:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _ship_hit(self):
        """处理外星人撞到飞船"""
        if self.status.ships_left > 0:
            # 剩余飞船-1
            self.status.ships_left -= 1
            self.scoreboard.prep_ships()

            # 清空余下的外星人和子弹
            self.bullets.empty()
            self.aliens.empty()

            # 创建新的外星人群和飞船
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.status.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船和外星人碰撞一样处理
                self._ship_hit()
                break


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()