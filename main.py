# -*- coding: Latin1 -*-
import pygame
import sys

from screen import Screen, GameOverScreen
from game_object import Player, Bullet
from game import Game
from music import init_music

def init_game():
    screen = Screen(bg_image)
    # Game objects initialization
    player = Player('img/player.png', 370, 480)
    bullet = Bullet('img/bullet.png', player.x, player.y)
    game = Game()

    return (screen, player, bullet, game)

def play_game(screen, player, bullet, game):
    running = True
    count = 0

    # Game loop
    while running:
        count += 1
        game_over = False
        screen.refresh_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.x_change = -20
                if event.key == pygame.K_RIGHT:
                    player.x_change = 20
                if event.key == pygame.K_SPACE and bullet.state == "ready":
                    bullet_sound.play()
                    bullet.fire_bullet(screen.screen, player.x, player.y)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.x_change = 0

        # Player move
        player.move()

        # Bullet move
        bullet.move(player.x, player.y)

        # Enemies move
        for enemy in game.enemies_list:
            continues = enemy.move()
            # Game over
            if not continues:
                enemies_to_erase = (enemy for enemy in game.enemies_list if enemy.y < 444)
                for enemy_to_erase in enemies_to_erase:
                    # Make enemies disappear
                    enemy_to_erase.y = 2000
                game_over = True
                running = False

            # Collision check
            collision = enemy.is_collision(bullet.x, bullet.y)
            if collision:
                game.collide(bullet, enemy, explosion_sound)

        game.drop_enemies(num_of_enemies)

        screen.update_screen(game.enemies_list, player, bullet, game.score, game_over)
        screen.draw_score(game.score)

    # After loop exit, create the GameOverScreen
    game_over_screen = GameOverScreen(bg_image)
    play_game_over(game_over_screen)


def play_game_over(game_over_screen):
    running = True
    retry_button = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if retry_button is not None:
                        if retry_button.collidepoint(event.pos):
                            # Reinit enemies list
                            screen, player, bullet, game = init_game()
                            play_game(screen, player, bullet, game)
                            print('click')

        retry_button = game_over_screen.update_screen()


if __name__ == '__main__':
    pygame.init()
    pygame.key.set_repeat(20)

    bullet_sound, explosion_sound = init_music()
    num_of_enemies = 6

    bg_image = pygame.image.load('img/background.jpg')

    screen, player, bullet, game = init_game()
    play_game(screen, player, bullet, game)
