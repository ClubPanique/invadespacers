import random

from game_object import Enemy


class Game:
    def __init__(self):
        self.score = 0
        self.enemies_list = []

    def drop_enemies(self, max_enemies):
        delay = random.random()
        if len(self.enemies_list) < max_enemies and delay < 0.8:
            for i in range(max_enemies - len(self.enemies_list)):
                enemy = Enemy()
                self.enemies_list.append(enemy)

    def refresh_enemies(self, max_enemies):
        self.enemies_list.clear()
        self.drop_enemies(max_enemies)

    def collide(self, bullet, enemy, explosion_sound):
        bullet.y = 480
        bullet.state = "ready"
        self.score += 1
        self.enemies_list.remove(enemy)
        explosion_sound.play()
        enemy_replace = Enemy()
        self.enemies_list.append(enemy_replace)