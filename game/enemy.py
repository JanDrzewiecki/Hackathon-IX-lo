import os
import pygame
from settings import*
from hit_box import*

class Enemy:
    # Cache heart images at class level to avoid reloading per instance
    HEART_IMG = None
    HEART_DIM = None
    HEART_SIZE = 22
    DEFAULT_HEARTS = 3

    @classmethod
    def _ensure_heart_imgs(cls):
        if cls.HEART_IMG is not None and cls.HEART_DIM is not None:
            return
        try:
            candidate = os.path.join(os.path.dirname(__file__), 'heart2.png')
            img = pygame.image.load(candidate).convert_alpha()
            img = pygame.transform.smoothscale(img, (cls.HEART_SIZE, cls.HEART_SIZE))
            cls.HEART_IMG = img
            dim = img.copy()
            shade = pygame.Surface((cls.HEART_SIZE, cls.HEART_SIZE), pygame.SRCALPHA)
            shade.fill((160, 160, 160, 255))
            try:
                dim.blit(shade, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            except Exception:
                dim.blit(shade, (0, 0))
            dim.set_alpha(160)
            cls.HEART_DIM = dim
        except Exception:
            cls.HEART_IMG = None
            cls.HEART_DIM = None

    def __init__(self, x, y, room=None, max_hearts=None):
        self.x = x
        self.y = y
        self.hp = 50
        self.ad = 10
        self.movement = 2
        self.hit_box = HitBox(self.x, self.y, PLAYER_SIZE//2 - 2, PLAYER_SIZE//2)
        self.room = room
        # Hearts-based health
        self.max_hearts = max_hearts if max_hearts is not None else self.DEFAULT_HEARTS
        self.hearts = self.max_hearts
        Enemy._ensure_heart_imgs()

    def set_room(self, room):
        """Set the room boundaries for this enemy."""
        self.room = room

    def take_hit(self) -> bool:
        """Apply one hit and return True if enemy is dead."""
        self.hearts = max(0, self.hearts - 1)
        return self.hearts == 0

    def draw(self, screen):
        # Enemy body
        pygame.draw.rect(screen, "red", (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))
        # Hearts above enemy using image sprites when available (no halves)
        slots = self.max_hearts
        spacing = 1
        size = Enemy.HEART_SIZE
        total_w = slots * size + (slots - 1) * spacing
        base_x = int(self.x + (PLAYER_SIZE - total_w) // 2)
        base_y = int(self.y - size - 4)
        use_img = Enemy.HEART_IMG is not None and Enemy.HEART_DIM is not None
        for i in range(slots):
            hx = base_x + i * (size + spacing)
            if use_img:
                img = Enemy.HEART_IMG if i < self.hearts else Enemy.HEART_DIM
                screen.blit(img, (hx, base_y))
            else:
                color = (220, 30, 30) if i < self.hearts else (80, 80, 80)
                pygame.draw.rect(screen, color, (hx, base_y, size, size), border_radius=size//4)

    def update(self, player_x, player_y):
        #calculating direction to the player
        vx = self.x - player_x
        vy = self.y - player_y
        normalize_factor = (vx ** 2 + vy ** 2) ** 0.5

        # Avoid division by zero when enemy is at same position as player
        if normalize_factor == 0:
            return

        vx /= normalize_factor
        vy /= normalize_factor
        #updating position
        new_x = self.x - vx * self.movement
        new_y = self.y - vy * self.movement

        # Clamp position to room boundaries if room is set
        if self.room:
            new_x, new_y = self.room.clamp_position(new_x, new_y, PLAYER_SIZE)

        self.x = new_x
        self.y = new_y
        self.hit_box.update_position(self.x, self.y)
