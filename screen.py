import pygame
import time


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


class Screen:
    def __init__(self, background, width=800, height=600, font_type='space_age.ttf', font_size=20, clock_tick=0):
        self.background = background
        self.WIDTH = width
        self.HEIGHT = height
        self.font_type = font_type
        self.font_size = font_size
        self.clock = pygame.time.Clock()
        self.clock_tick = clock_tick

        self.fonts = self.init_fonts()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Space Invaders")
        icon = pygame.image.load('img/si_logo.jpg')
        pygame.display.set_icon(icon)

    def init_fonts(self):
        fonts = {
            "20": pygame.font.Font(self.font_type, 20),
            "32": pygame.font.Font(self.font_type, 32),
            "64": pygame.font.Font(self.font_type, 64),
        }
        return fonts

    def refresh_screen(self):
        self.screen.blit(self.background, (0, 0))

    def draw_player_line(self, player, count, game_over):
        if not game_over:
            self.draw_dash_line(player)
        else:
            # Makes the line flash
            if count % 2 == 0:
                self.draw_dash_line(player)

    def draw_dash_line(self, player):
        x = 0
        while x < self.WIDTH:
            width = 5
            if (x < player.x - 10) or (x > player.x + 70):
                pygame.draw.rect(self.screen, (255, 255, 255), (x, 480, width, 2))
            x += 10

    def draw_enemies(self, enemies_list, count=0):
        for enemy in enemies_list:
            if count % 2 == 0:
                enemy.draw(self.screen)

    def draw_player(self, player):
        player.draw(self.screen)

    def draw_bullet(self, bullet):
        if bullet.state == 'fire':
            bullet.draw(self.screen)

    def draw_score(self, score):
        text_x = text_y = 10
        score = self.fonts["32"].render("Score : " + str(score), True, (255, 255, 255))
        self.screen.blit(score, (text_x, text_y))

    def update_screen(self, enemies_list, player, bullet, score, game_over):
        if game_over:
            for i in range(20):
                self.refresh_screen()
                self.draw_enemies(enemies_list, count=i)
                self.draw_player(player)
                self.draw_player_line(player, i, game_over)
                self.draw_bullet(bullet)
                self.draw_score(score)
                pygame.display.update()
                self.clock.tick(self.clock_tick + 30)
                time.sleep(0.1)
        else:
            self.refresh_screen()
            self.draw_enemies(enemies_list)
            self.draw_player(player)
            self.draw_player_line(player, 0, game_over)
            self.draw_bullet(bullet)
            self.draw_score(score)
            pygame.display.update()
            self.clock.tick(self.clock_tick)


class GameOverScreen(Screen):
    def __init__(self,  background, width=800, height=600, font_type='space_age.ttf', font_size=20, clock_tick=0):
        super().__init__(background, width, height, font_type, font_size, clock_tick)

    def update_screen(self):
        self.refresh_screen()

        self.draw_game_over()
        retry_button = self.draw_retry_button()

        pygame.display.update()

        return retry_button

    def draw_game_over(self):
        over_surf, over_rect = text_objects('GAME OVER', self.fonts["64"], (255, 255, 255))
        over_rect.center = (round(self.WIDTH / 2), round(self.HEIGHT / 2))
        self.screen.blit(over_surf, over_rect)

    def draw_retry_button(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (330, 340, 150, 50))
        retry_surf, retry_rect = text_objects('Retry?', self.fonts["20"], (0, 0, 0))
        retry_rect.center = (round(330 + (150 / 2)), round(340 + (50 / 2)))
        self.screen.blit(retry_surf, retry_rect)
        return retry_rect
