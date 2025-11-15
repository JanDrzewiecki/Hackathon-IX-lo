"""Enemy bullet class for boss attacks"""
import pygame
from hit_box import HitBox
from settings import *


class EnemyBullet:
    def __init__(self, enemy_x, enemy_y, target_x, target_y):
        self.x = enemy_x
        self.y = enemy_y
        self.ad = 20 # Damage to player

        # Calculate direction
        self.vx = target_x - self.x
        self.vy = target_y - self.y
        normalize_factor = (self.vx ** 2 + self.vy ** 2) ** 0.5

        if normalize_factor > 0:
            self.vx /= normalize_factor
            self.vy /= normalize_factor

        self.r = 8  # Bullet radius
        self.movement = 4  # Speed (reduced from 6 to 4 - slower)
        self.hit_box = HitBox(self.x, self.y, self.r, self.r)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 50, 50), (int(self.x), int(self.y)), self.r)

    def update(self):
        self.x += self.vx * self.movement
        self.y += self.vy * self.movement
        self.hit_box.update_position(self.x, self.y)

