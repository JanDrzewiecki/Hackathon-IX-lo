import random
import pygame
from settings import *
from enemy import *
from enemy_type import EnemyType, EnemyTypeConfig


class EnemySpawner:
    def __init__(self, level, room_manager=None):
        self.level = level
        self.cooldown_limit = FPS / 2
        self.cooldown = 0
        self.room_manager = room_manager
        self.enemies_spawned_in_room = 0
        self.max_enemies_for_room = 0

    def update_level(self, level):
        self.level = level
        self.cooldown_limit -= 1

    def set_room_manager(self, room_manager):
        """Set the room manager."""
        self.room_manager = room_manager

    def reset_for_new_room(self):
        """Reset spawner when entering a new room"""
        if self.room_manager:
            current_room = self.room_manager.rooms[self.room_manager.current_room_id]
            enemy_type = current_room.enemy_type
            self.max_enemies_for_room = EnemyTypeConfig.get_count(enemy_type)
            self.enemies_spawned_in_room = 0

    def update(self, enemies: list[Enemy]):
        # If we haven't set max enemies for current room, do it now
        if self.max_enemies_for_room == 0 and self.room_manager:
            self.reset_for_new_room()

        self.cooldown += 1
        if self.cooldown >= self.cooldown_limit:
            self.cooldown = 0

            # Check if we should spawn more enemies
            if self.enemies_spawned_in_room >= self.max_enemies_for_room:
                return

            # Spawn enemy based on current room's enemy type
            if self.room_manager:
                current_room = self.room_manager.rooms[self.room_manager.current_room_id]
                enemy_type = current_room.enemy_type

                # Get spawn position at room edges
                x, y = self.room_manager.get_random_spawn_position()

                # Create enemy with specific type and level
                enemy = Enemy(x, y, enemy_type, self.room_manager, level=self.level)
                enemies.append(enemy)
                self.enemies_spawned_in_room += 1
            else:
                # Fallback to screen edges if no room manager is set
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

                enemy = Enemy(x, y, EnemyType.WEAK, None, level=self.level)
                enemies.append(enemy)


