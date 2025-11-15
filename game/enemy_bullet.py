"""Enemy bullet class for boss attacks"""
import pygame
from hit_box import HitBox
from settings import *
import math


class EnemyBullet:
    # Cached sprite for all bullets
    _sprite = None
    _sprite_size = 48  # Size of the fireball sprite (scaled for visibility)

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

        self.r = 16  # Bullet radius (increased for sprite)
        self.movement = 4  # Speed (reduced from 6 to 4 - slower)
        self.hit_box = HitBox(self.x, self.y, self.r, self.r)

        # Calculate rotation angle for sprite
        self.angle = math.degrees(math.atan2(self.vy, self.vx))

        # Load sprite if not already loaded
        if EnemyBullet._sprite is None:
            try:
                try:
                    sprite = pygame.image.load("game/coal-boss-fire.png").convert_alpha()
                except:
                    sprite = pygame.image.load("coal-boss-fire.png").convert_alpha()
                EnemyBullet._sprite = pygame.transform.smoothscale(sprite, (self._sprite_size, self._sprite_size))
            except Exception as e:
                print(f"Error loading coal-boss-fire.png: {e}")
                EnemyBullet._sprite = None

    def draw(self, screen):
        if EnemyBullet._sprite:
            # Rotate sprite to face direction of movement
            rotated_sprite = pygame.transform.rotate(EnemyBullet._sprite, -self.angle)
            sprite_rect = rotated_sprite.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(rotated_sprite, sprite_rect)
        else:
            # Fallback to circle if sprite failed to load
            pygame.draw.circle(screen, (255, 50, 50), (int(self.x), int(self.y)), self.r)

    def update(self):
        self.x += self.vx * self.movement
        self.y += self.vy * self.movement
        self.hit_box.update_position(self.x, self.y)

