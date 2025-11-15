"""Enemy bullet class for boss attacks"""
import pygame
from hit_box import HitBox
from settings import *
import math


class EnemyBullet:
    # Cached sprites for different boss types
    _coal_sprite = None  # Level 1 coal boss fire
    _trash_sprites = [None, None, None]  # Level 2 trash boss fires (1, 2, 3)
    _final_sprite = None  # Level 3 final boss fire
    _sprite_size = 48  # Size of the fireball sprite (scaled for visibility)

    def __init__(self, enemy_x, enemy_y, target_x, target_y, level=1, fire_sprite_index=0):
        self.x = enemy_x
        self.y = enemy_y
        self.ad = 30 # Damage to player (increased from 20 to 30)
        self.level = level
        self.fire_sprite_index = fire_sprite_index

        # Calculate direction
        self.vx = target_x - self.x
        self.vy = target_y - self.y
        normalize_factor = (self.vx ** 2 + self.vy ** 2) ** 0.5

        if normalize_factor > 0:
            self.vx /= normalize_factor
            self.vy /= normalize_factor

        self.r = 16  # Bullet radius (increased for sprite)
        self.movement = 6  # Speed (increased from 4 to 6 - faster by ~0.3s)
        self.hit_box = HitBox(self.x, self.y, self.r, self.r)

        # Calculate rotation angle for sprite
        self.angle = math.degrees(math.atan2(self.vy, self.vx))

        # Load appropriate sprite based on level
        self._load_sprite()

    def _load_sprite(self):
        """Load the appropriate fire sprite based on level and index"""
        if self.level == 2:
            # Trash boss - load all 3 sprites if not already loaded
            sprite_names = ["trash-boss-fire1.png", "trash-boss-fire2.png", "trash-boss-fire3.png"]
            for i, sprite_name in enumerate(sprite_names):
                if EnemyBullet._trash_sprites[i] is None:
                    try:
                        try:
                            sprite = pygame.image.load(f"game/{sprite_name}").convert_alpha()
                        except:
                            sprite = pygame.image.load(sprite_name).convert_alpha()
                        EnemyBullet._trash_sprites[i] = pygame.transform.smoothscale(sprite, (self._sprite_size, self._sprite_size))
                    except Exception as e:
                        print(f"Error loading {sprite_name}: {e}")
                        EnemyBullet._trash_sprites[i] = None
            # Set current sprite for this bullet
            self.sprite = EnemyBullet._trash_sprites[self.fire_sprite_index]
        elif self.level == 4:
            # Final boss (level 4)
            if EnemyBullet._final_sprite is None:
                try:
                    try:
                        sprite = pygame.image.load("game/final-boss-fire.png").convert_alpha()
                    except:
                        sprite = pygame.image.load("final-boss-fire.png").convert_alpha()
                    EnemyBullet._final_sprite = pygame.transform.smoothscale(sprite, (self._sprite_size, self._sprite_size))
                except Exception as e:
                    print(f"Error loading final-boss-fire.png: {e}")
                    EnemyBullet._final_sprite = None
            self.sprite = EnemyBullet._final_sprite
        else:
            # Coal boss (level 1 and 3) and default
            if EnemyBullet._coal_sprite is None:
                try:
                    try:
                        sprite = pygame.image.load("game/coal-boss-fire.png").convert_alpha()
                    except:
                        sprite = pygame.image.load("coal-boss-fire.png").convert_alpha()
                    EnemyBullet._coal_sprite = pygame.transform.smoothscale(sprite, (self._sprite_size, self._sprite_size))
                except Exception as e:
                    print(f"Error loading coal-boss-fire.png: {e}")
                    EnemyBullet._coal_sprite = None
            self.sprite = EnemyBullet._coal_sprite

    def draw(self, screen):
        if self.sprite:
            # Rotate sprite to face direction of movement
            rotated_sprite = pygame.transform.rotate(self.sprite, -self.angle)
            sprite_rect = rotated_sprite.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(rotated_sprite, sprite_rect)
        else:
            # Fallback to circle if sprite failed to load
            pygame.draw.circle(screen, (255, 50, 50), (int(self.x), int(self.y)), self.r)

    def update(self):
        self.x += self.vx * self.movement
        self.y += self.vy * self.movement
        self.hit_box.update_position(self.x, self.y)

