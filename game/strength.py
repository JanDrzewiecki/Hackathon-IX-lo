import pygame
from hit_box import HitBox

class Strength:
    """
    Pickup item that grants temporary double attack damage when activated.
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.alive = True
        # Load image (try common names); fallback to sword-like rectangle
        img = None
        for path in (
            "game/swordbg.png",
            "swordbg.png",
            "game/sword.png",
            "sword.png",
        ):
            try:
                img = pygame.image.load(path).convert_alpha()
                break
            except Exception:
                img = None
        if img is None:
            # Fallback: simple sword-like surface
            size = 48
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.rect(surf, (180, 180, 180), (size//3, 4, size//6, size-8))
            pygame.draw.polygon(surf, (200, 200, 200), [(size//2, 0), (size//2 - 6, 8), (size//2 + 6, 8)])
            img = surf
        else:
            img = pygame.transform.smoothscale(img, (48, 48))
        self.sprite = img
        # Circular collision via HitBox; use radius ~ 20, offset = 24 to center
        self.hit_box = HitBox(self.x, self.y, r=20, size_offset=24)

    def draw(self, screen):
        if not self.alive:
            return
        screen.blit(self.sprite, (self.x, self.y))

    def update_position(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hit_box.update_position(x, y)

