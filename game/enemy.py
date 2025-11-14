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

        # Prepare heart icons once (shared)
        self._ensure_hearts_loaded()

    def _ensure_hearts_loaded(self):
        if Enemy._heart_img is None or Enemy._dim_heart_img is None:
            heart, dim = load_heart_images(16, './heart2.png')
            Enemy._heart_img = heart
            Enemy._dim_heart_img = dim

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
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        # Draw hearts above enemy
        self._draw_enemy_hearts(screen)

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
