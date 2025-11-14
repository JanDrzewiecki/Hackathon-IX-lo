import random

import  pygame
from settings import*
from enemy import*

class EnemySpawner:
    def __init__(self, level, room=None):
        self.level = level
        self.cooldown_limit = FPS / 2
        self.cooldown = 0
        self.room = room

    def update_level(self, level):
        self.level = level
        self.cooldown_limit -= 1

    def set_room(self, room):
        """Set the room where enemies should spawn."""
        self.room = room

    def update(self, enemies: list[Enemy]):
        self.cooldown += 1
        if self.cooldown >= self.cooldown_limit:
            self.cooldown = 0
            # spawn
            if self.room:
                # Spawn at room edges
                x, y = self.room.get_random_spawn_position()
            else:
                # Fallback to screen edges if no room is set
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

            enemy = Enemy(x, y, self.room)
            enemies.append(enemy)


