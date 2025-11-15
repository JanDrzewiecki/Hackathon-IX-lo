import pygame
from settings import *
from hit_box import *
from enemy_type import EnemyType, EnemyTypeConfig
from hud import load_heart_images


class Enemy:
    # Cached heart images for all enemies to avoid reloading each frame
    _heart_img = None
    _dim_heart_img = None

    def __init__(self, x, y, enemy_type=EnemyType.WEAK, room=None):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type

        # Get stats from enemy type config
        config = EnemyTypeConfig.get_config(enemy_type)
        self.hp = config['hp']
        self.max_hp = config['hp']
        self.ad = config['ad']
        self.movement = config['speed']
        self.color = config['color']
        self.size = config['size']

        self.hit_box = HitBox(self.x, self.y, self.size // 2 - 2, self.size // 2)
        self.room = room

        # Animation properties
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 8  # Animation speed
        self.frames = []
        self.current_sprite = None
        self.facing_left = False  # Track if enemy is facing left

        # Load sprite sheet based on enemy type
        if self.enemy_type == EnemyType.WEAK:
            self.frames = self.load_sheet("enemy1.png", 100, 100)
            if self.frames:
                self.current_sprite = self.frames[0]
        elif self.enemy_type == EnemyType.MEDIUM:
            self.frames = self.load_sheet("enemy2.png", 100, 100)
            if self.frames:
                self.current_sprite = self.frames[0]

        # Prepare heart icons once (shared)
        self._ensure_hearts_loaded()

    def _ensure_hearts_loaded(self):
        if Enemy._heart_img is None or Enemy._dim_heart_img is None:
            heart, dim = load_heart_images(16, './heart2.png')
            Enemy._heart_img = heart
            Enemy._dim_heart_img = dim

    def load_sheet(self, path, frame_width, frame_height):
        """Load sprite sheet and split it into individual frames"""
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
                frames.append(frame)

            return frames
        except Exception as e:
            print(f"Error loading enemy sprite {path}: {e}")
            return []

    def set_room(self, room):
        """Set the room boundaries for this enemy."""
        self.room = room

    def _draw_enemy_hearts(self, screen):
        # Each heart represents 10 HP (as per example: 50 HP -> 5 hearts)
        hp_per_heart = 10
        total_hearts = max(1, int((self.max_hp + hp_per_heart - 1) // hp_per_heart))

        # Visual size of hearts relative to enemy size
        heart_size = max(10, min(20, int(self.size * 0.4)))
        spacing = 2
        # If we just loaded default size 16 previously, but heart_size differs, rescale once
        if Enemy._heart_img is not None and Enemy._heart_img.get_width() != heart_size:
            try:
                Enemy._heart_img = pygame.transform.smoothscale(Enemy._heart_img, (heart_size, heart_size))
                Enemy._dim_heart_img = pygame.transform.smoothscale(Enemy._dim_heart_img, (heart_size, heart_size))
            except Exception:
                pass

        total_width = total_hearts * heart_size + (total_hearts - 1) * spacing
        x0 = self.x + (self.size - total_width) // 2
        y0 = self.y - heart_size - 4

        # Compute how many hearts are fully/partially filled based on current HP in units of 10
        shown_hp = max(0, min(self.hp, self.max_hp))
        hearts_value = shown_hp / float(hp_per_heart)

        use_fallback = (Enemy._heart_img is None or Enemy._dim_heart_img is None)

        for i in range(total_hearts):
            x = x0 + i * (heart_size + spacing)
            filled = hearts_value - i  # 1.0 = full, 0.0 = empty, in-between = partial
            if filled <= 0:
                if use_fallback:
                    # Draw dim rect
                    s = pygame.Surface((heart_size, heart_size), pygame.SRCALPHA)
                    pygame.draw.rect(s, (80, 80, 80, 140), s.get_rect(), border_radius=heart_size // 4)
                    screen.blit(s, (x, y0))
                else:
                    screen.blit(Enemy._dim_heart_img, (x, y0))
                continue
            if use_fallback:
                # Draw dim background then filled portion as red rect
                s = pygame.Surface((heart_size, heart_size), pygame.SRCALPHA)
                pygame.draw.rect(s, (80, 80, 80, 140), s.get_rect(), border_radius=heart_size // 4)
                screen.blit(s, (x, y0))
                w = heart_size if filled >= 1 else max(1, int(filled * heart_size))
                fg = pygame.Surface((w, heart_size), pygame.SRCALPHA)
                pygame.draw.rect(fg, (220, 30, 30, 255), fg.get_rect(), border_radius=heart_size // 4)
                screen.blit(fg, (x, y0))
            else:
                if filled >= 1:
                    screen.blit(Enemy._heart_img, (x, y0))
                else:
                    # Draw dim then overlay clipped heart for partial fill
                    screen.blit(Enemy._dim_heart_img, (x, y0))
                    w = max(1, int(filled * heart_size))
                    area = pygame.Rect(0, 0, w, heart_size)
                    screen.blit(Enemy._heart_img, (x, y0), area=area)

    def draw(self, screen):
        # Draw animated sprite for WEAK and MEDIUM enemies, otherwise draw colored square
        if (self.enemy_type == EnemyType.WEAK or self.enemy_type == EnemyType.MEDIUM) and self.current_sprite:
            # Flip sprite horizontally if facing left
            if self.facing_left:
                flipped_sprite = pygame.transform.flip(self.current_sprite, True, False)
                sprite_rect = flipped_sprite.get_rect(center=(int(self.x + self.size // 2), int(self.y + self.size // 2)))
                screen.blit(flipped_sprite, sprite_rect)
            else:
                sprite_rect = self.current_sprite.get_rect(center=(int(self.x + self.size // 2), int(self.y + self.size // 2)))
                screen.blit(self.current_sprite, sprite_rect)
        else:
            # Draw colored square for other enemy types (STRONG)
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

        # Draw hearts above enemy
        self._draw_enemy_hearts(screen)

    def update(self, player_x, player_y):
        # Update animation for WEAK and MEDIUM enemies
        if (self.enemy_type == EnemyType.WEAK or self.enemy_type == EnemyType.MEDIUM) and self.frames:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_speed:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.current_sprite = self.frames[self.frame_index]

        # calculating direction to the player
        vx = self.x - player_x
        vy = self.y - player_y
        normalize_factor = (vx ** 2 + vy ** 2) ** 0.5

        # Avoid division by zero when enemy is at same position as player
        if normalize_factor == 0:
            return

        vx /= normalize_factor
        vy /= normalize_factor

        # Track facing direction based on horizontal movement
        # vx > 0 means enemy is to the right of player, so moving left (towards player) - normal sprite
        # vx < 0 means enemy is to the left of player, so moving right (towards player) - flip sprite
        if vx > 0:
            self.facing_left = False  # Moving left - normal sprite
        elif vx < 0:
            self.facing_left = True  # Moving right - flip sprite

        # updating position
        new_x = self.x - vx * self.movement
        new_y = self.y - vy * self.movement

        # Clamp position to room boundaries if room is set
        if self.room:
            new_x, new_y = self.room.clamp_position(new_x, new_y, self.size)

        self.x = new_x
        self.y = new_y
        self.hit_box.update_position(self.x, self.y)
