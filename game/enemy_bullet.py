"""Enemy bullet class for boss attacks"""
import pygame
from hit_box import HitBox
from settings import *
import math


class EnemyBullet:
    # Cached sprites for different boss types
    _coal_sprite = None  # Level 1 coal boss fire
    _trash_sprites = [None, None, None]  # Level 2 trash boss fires (1, 2, 3)
    _olejman_sprite = None  # Level 3 olejman boss fire
    _final_sprite_frames = None  # Level 4 final boss fire animation frames
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

        # Bullet radius - much larger for Olejman boss (level 3)
        self.r = 100 if level == 3 else 16  # 100 for 200x200 sprite, 16 for normal
        self.movement = 6  # Speed (increased from 4 to 6 - faster by ~0.3s)
        self.hit_box = HitBox(self.x, self.y, self.r, self.r)

        # Calculate rotation angle for sprite
        self.angle = math.degrees(math.atan2(self.vy, self.vx))

        # Animation properties for final boss
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 5  # Animation speed (lower = faster)
        self.frames = None
        self.current_sprite = None

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
        elif self.level == 3:
            # Olejman boss (level 3) - Huge 200x200 bullet
            if EnemyBullet._olejman_sprite is None:
                try:
                    try:
                        sprite = pygame.image.load("game/olejman-boss-fire.png").convert_alpha()
                    except:
                        sprite = pygame.image.load("olejman-boss-fire.png").convert_alpha()
                    # Scale to 200x200 (huge bullet)
                    EnemyBullet._olejman_sprite = pygame.transform.smoothscale(sprite, (200, 200))
                except Exception as e:
                    print(f"Error loading olejman-boss-fire.png: {e}")
                    EnemyBullet._olejman_sprite = None
            self.sprite = EnemyBullet._olejman_sprite
        elif self.level == 4:
            # Final boss (level 4) - Load animated sprite sheet (600x100 = 4 frames of 150x100)
            if EnemyBullet._final_sprite_frames is None:
                EnemyBullet._final_sprite_frames = self._load_sheet("final-boss-fire.png", 150, 100)

            # Each bullet gets its own frames (reference to cached frames)
            self.frames = EnemyBullet._final_sprite_frames
            if self.frames:
                self.current_sprite = self.frames[0]
            self.sprite = None  # Don't use single sprite for final boss
        else:
            # Coal boss (level 1) and default
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

    def _load_sheet(self, path, frame_width, frame_height):
        """Load sprite sheet and split it into individual frames (for final boss animation)"""
        try:
            try:
                sheet = pygame.image.load(f"game/{path}").convert_alpha()
            except:
                sheet = pygame.image.load(path).convert_alpha()

            sheet_width, sheet_height = sheet.get_size()
            cols = sheet_width // frame_width
            frames = []

            for col in range(cols):
                rect = pygame.Rect(col * frame_width, 0, frame_width, frame_height)
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), rect)
                # Scale frame to sprite size
                scaled_frame = pygame.transform.smoothscale(frame, (self._sprite_size, self._sprite_size))
                frames.append(scaled_frame)

            return frames
        except Exception as e:
            print(f"Error loading sprite sheet {path}: {e}")
            return []

    def draw(self, screen):
        # For final boss (level 4), use animated sprite
        if self.level == 4 and self.current_sprite:
            # Rotate sprite to face direction of movement
            rotated_sprite = pygame.transform.rotate(self.current_sprite, -self.angle)
            sprite_rect = rotated_sprite.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(rotated_sprite, sprite_rect)
        elif self.sprite:
            # For other bosses, use single sprite
            # Rotate sprite to face direction of movement
            rotated_sprite = pygame.transform.rotate(self.sprite, -self.angle)
            sprite_rect = rotated_sprite.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(rotated_sprite, sprite_rect)
        else:
            # Fallback to circle if sprite failed to load
            pygame.draw.circle(screen, (255, 50, 50), (int(self.x), int(self.y)), self.r)

    def update(self):
        # Update animation for final boss bullets
        if self.level == 4 and self.frames:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_speed:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.current_sprite = self.frames[self.frame_index]

        # Update position
        self.x += self.vx * self.movement
        self.y += self.vy * self.movement
        self.hit_box.update_position(self.x, self.y)

