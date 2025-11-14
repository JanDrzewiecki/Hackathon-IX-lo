import os
import pygame

class HeartsHUD:
    def __init__(self, hp_per_heart: int = 20, heart_size: int = 60, spacing: int = 2,
                 pos=(10, 10), image_path: str = './heart2.png'):
        self.hp_per_heart = hp_per_heart
        self.heart_size = heart_size
        self.spacing = spacing
        self.x0, self.y0 = pos

        self.heart = None
        self.dim_heart = None

        # Resolve image path relative to this file to avoid CWD issues
        resolved_path = None
        if image_path:
            if os.path.isabs(image_path) and os.path.exists(image_path):
                resolved_path = image_path
            else:
                # Try given path relative to CWD first, then relative to this file
                if os.path.exists(image_path):
                    resolved_path = image_path
                else:
                    candidate = os.path.join(os.path.dirname(__file__), image_path)
                    if os.path.exists(candidate):
                        resolved_path = candidate
        if resolved_path:
            try:
                img = pygame.image.load(resolved_path).convert_alpha()
                self.heart = pygame.transform.smoothscale(img, (heart_size, heart_size))

                dim = self.heart.copy()
                shade = pygame.Surface((heart_size, heart_size), pygame.SRCALPHA)
                shade.fill((160, 160, 160, 255))
                try:
                    dim.blit(shade, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                except Exception:
                    dim.blit(shade, (0, 0))
                dim.set_alpha(140)
                self.dim_heart = dim
            except Exception:
                self.heart = None
                self.dim_heart = None

    def _draw_fallback(self, surface: pygame.Surface, x: int, y: int, filled_ratio: float):
        # Draw only the filled portion; keep the rest transparent.
        size = self.heart_size
        if filled_ratio <= 0:
            return
        w = size if filled_ratio >= 1 else max(1, int(filled_ratio * size))
        fg = pygame.Surface((w, size), pygame.SRCALPHA)
        pygame.draw.rect(fg, (220, 30, 30, 255), fg.get_rect(), border_radius=size // 4)
        surface.blit(fg, (x, y))

    def draw(self, surface: pygame.Surface, player_obj):

        slots = min(3, max(1, player_obj.max_hp // self.hp_per_heart))
        max_shown = slots * self.hp_per_heart
        shown_hp = max(0, min(player_obj.hp, max_shown))

        use_fallback = (self.heart is None or self.dim_heart is None)

        for i in range(slots):
            x = self.x0 + i * (self.heart_size + self.spacing)
            y = self.y0

            # For transparency: do not draw any background for partially filled hearts.
            # Only draw the filled portion so the missing part remains transparent.

            filled = (shown_hp - i * self.hp_per_heart) / self.hp_per_heart
            if filled <= 0:
                # Empty slot: show dim heart (not fully transparent)
                if use_fallback:
                    size = self.heart_size
                    bg = pygame.Surface((size, size), pygame.SRCALPHA)
                    pygame.draw.rect(bg, (80, 80, 80, 140), bg.get_rect(), border_radius=size // 4)
                    surface.blit(bg, (x, y))
                else:
                    surface.blit(self.dim_heart, (x, y))
                continue
            if use_fallback:
                # Draw dim base first, then the filled portion so the missing part is dimmed/transparent
                size = self.heart_size
                bg = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.rect(bg, (80, 80, 80, 140), bg.get_rect(), border_radius=size // 4)
                surface.blit(bg, (x, y))
                self._draw_fallback(surface, x, y, filled_ratio=min(1.0, filled))
            else:
                if filled >= 1:
                    surface.blit(self.heart, (x, y))
                else:
                    # Draw dim background first so the missing part appears dimmed
                    surface.blit(self.dim_heart, (x, y))
                    w = max(1, int(filled * self.heart_size))
                    area = pygame.Rect(0, 0, w, self.heart_size)
                    surface.blit(self.heart, (x, y), area=area)
