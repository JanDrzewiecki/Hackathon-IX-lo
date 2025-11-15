import pygame
from hit_box import HitBox

class Shield:
    """
    Pickup item that grants temporary invulnerability when activated.
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.alive = True
        # Load image (try common names); fallback to blue circle
        img = None
        for path in (
            "game/shield.png",
            "shield.png",
            "game/shield.jpg.avif",
            "shield.jpg.avif",
            "game/boost_shield.png",
            "boost_shield.png",
        ):
            try:
                img = pygame.image.load(path).convert_alpha()
                break
            except Exception:
                img = None
        if img is None:
            # Fallback: blue circle icon
            size = 48
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surf, (80, 160, 255), (size//2, size//2), size//2)
            pygame.draw.circle(surf, (200, 230, 255), (size//2, size//2), size//2, 3)
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
