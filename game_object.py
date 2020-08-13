import pygame
import math
import random


class GameObject():
    def __init__(self, image, x, y, x_change, y_change):
        super().__init__()
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_collision(self, other_x, other_y):
        distance = math.sqrt((other_x - self.x) ** 2 + (other_y - self.y) ** 2)
        if distance < 27:
            return True
        else:
            return False

    def adjust_position(self):
        is_bound = False
        if self.x < 0:
            self.x = 0
            is_bound = True
        elif self.x > 736:
            self.x = 736
            is_bound = True
        return is_bound


class Player(GameObject):
    def __init__(self, image, x, y, x_change=0, y_change=0):
        super().__init__(image, x, y, x_change, y_change)

    def move(self):
        self.x += self.x_change
        self.adjust_position()


class Enemy(GameObject):
    def __init__(self, image='img/enemy_red.png', x_change=4, y_change=100):
        x = random.randint(0, 735)
        y = random.randint(30, 150)
        super().__init__(image, x, y, x_change, y_change)

    # Returns false if game over limit is reached
    def move(self):
        if self.y > 444:
            return False
        else:
            self.x += self.x_change
            is_at_corner = self.adjust_position()
            if is_at_corner:
                self.x_change *= -1
                self.y += self.y_change
            return True


class GreenEnemy(Enemy):
    def __init__(self,image='img/enemy_green_test.png', x_change=4, y_change=70):
        super().__init__(image, x_change, y_change)


class Bullet(GameObject):
    def __init__(self, image, x, y, state='ready', x_change=0, y_change=20):
        super().__init__(image, x, y, x_change, y_change)
        self.state = state

    def fire_bullet(self, screen, player_x, player_y):
        self.state = "fire"
        self.x, self.y = player_x + 24, player_y - 16
        screen.blit(self.image, (self.x, self.y))

    def move(self, player_x, player_y):
        if self.state == 'fire' and self.y <= 0:
            self.x = player_x
            self.y = player_y
            self.state = 'ready'
        if self.state == 'fire':
            self.y -= self.y_change
