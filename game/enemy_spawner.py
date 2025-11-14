import random

import  pygame
from settings import*
from enemy import*

class EnemySpawner:
    def __init__(self, level):
        self.level = level
        self.cooldown_limit = FPS / 2
        self.cooldown = 0

    def update_level(self, level):
        self.level = level
        self.cooldown_limit -= 1

    def update(self, enemies: list[Enemy]):
        self.cooldown += 1
        if self.cooldown >= self.cooldown_limit:
            self.cooldown = 0
            # spawn
            r = random.randint(0, 3)
            if r == 0:
                x = random.randint(0, SCREEN_WIDTH)
                y = 0
            elif r == 1:
                x = random.randint(0, SCREEN_WIDTH)
                y = SCREEN_HEIGHT
            elif r == 2:
                y = random.randint(0, SCREEN_HEIGHT)
                x = 0
            else:
                y = random.randint(0, SCREEN_HEIGHT)
                x = SCREEN_WIDTH - ENEMY_SIZE

            enemies.append(Enemy(x,y))
