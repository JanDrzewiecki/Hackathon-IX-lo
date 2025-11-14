import pygame
from settings import *
from hit_box import *
from enemy_type import EnemyType, EnemyTypeConfig


class Enemy:
    def __init__(self, x, y, enemy_type=EnemyType.WEAK, room=None):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type

        # Get stats from enemy type config
        config = EnemyTypeConfig.get_config(enemy_type)
        self.hp = config['hp']
        self.ad = config['ad']
        self.movement = config['speed']
        self.color = config['color']
        self.size = config['size']

        self.hit_box = HitBox(self.x, self.y, self.size // 2 - 2, self.size // 2)
        self.room = room

    def set_room(self, room):
        """Set the room boundaries for this enemy."""
        self.room = room

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def update(self, player_x, player_y):
        # calculating direction to the player
        vx = self.x - player_x
        vy = self.y - player_y
        normalize_factor = (vx ** 2 + vy ** 2) ** 0.5

        # Avoid division by zero when enemy is at same position as player
        if normalize_factor == 0:
            return

        vx /= normalize_factor
        vy /= normalize_factor
        # updating position
        new_x = self.x - vx * self.movement
        new_y = self.y - vy * self.movement

        # Clamp position to room boundaries if room is set
        if self.room:
            new_x, new_y = self.room.clamp_position(new_x, new_y, self.size)

        self.x = new_x
        self.y = new_y
        self.hit_box.update_position(self.x, self.y)
