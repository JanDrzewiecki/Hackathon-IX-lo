import pygame
from hit_box import HitBox

class Shoe:
    """
    Simple pickup item that grants a temporary speed boost when collected.
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.alive = True
        # Load image
        img = None
        try:
            img = pygame.image.load("game/boost_shoe2.png").convert_alpha()
        except Exception:
            try:
                img = pygame.image.load("boost_shoe2.png").convert_alpha()
            except Exception:
                img = None
        if img is None:
            # Fallback: small red square if image missing
            img = pygame.Surface((48, 48), pygame.SRCALPHA)
            img.fill((220, 60, 60))
        # Scale to a reasonable size (48x48)
        self.sprite = pygame.transform.smoothscale(img, (48, 48))
        # Circular collision via HitBox; use radius ~ 20, offset = 24 to center
        self.hit_box = HitBox(self.x, self.y, r=20, size_offset=24)

    def draw(self, screen):
        if not self.alive:
            return
        screen.blit(self.sprite, (self.x, self.y))

    def update_position(self, x: int, y: int):
        """If we ever need to move the shoe."""
        self.x = x
        self.y = y
        self.hit_box.update_position(x, y)
