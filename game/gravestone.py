import pygame
from hit_box import HitBox


class Gravestone:
    """A gravestone/rip marker that appears where an enemy died"""

    # Class variable to cache the loaded image
    _rip_image = None

    def __init__(self, x, y, enemy_size):
        """
        Create a gravestone at the enemy's death position

        Args:
            x: X position of dead enemy
            y: Y position of dead enemy
            enemy_size: Size of the enemy that died (used to scale gravestone)
        """
        self.x = x
        self.y = y
        self.enemy_size = enemy_size
        self.size = enemy_size

        # Create hitbox for collision detection
        # Use radius = size/2 and offset = size/2 to center the circular hitbox on the gravestone
        self.hit_box = HitBox(self.x, self.y, self.size // 2, self.size // 2)

        # Load and cache the rip image
        if Gravestone._rip_image is None:
            try:
                Gravestone._rip_image = pygame.image.load("game/rip.png").convert_alpha()
            except:
                try:
                    Gravestone._rip_image = pygame.image.load("rip.png").convert_alpha()
                except Exception as e:
                    print(f"Warning: Could not load rip.png: {e}")
                    Gravestone._rip_image = None

        # Scale the image to match enemy size
        if Gravestone._rip_image:
            self.image = pygame.transform.smoothscale(
                Gravestone._rip_image,
                (enemy_size, enemy_size)
            )
        else:
            # Fallback: create a simple gray rectangle if image fails to load
            self.image = pygame.Surface((enemy_size, enemy_size), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (100, 100, 100), self.image.get_rect())
            # Draw "RIP" text on fallback
            try:
                font = pygame.font.SysFont("Arial", max(10, enemy_size // 4))
                text = font.render("RIP", True, (255, 255, 255))
                text_rect = text.get_rect(center=(enemy_size // 2, enemy_size // 2))
                self.image.blit(text, text_rect)
            except:
                pass

    def update_position(self, x, y):
        """Update gravestone position and hitbox"""
        self.x = x
        self.y = y
        self.hit_box.update_position(self.x, self.y)

    def draw(self, screen):
        """Draw the gravestone on screen"""
        screen.blit(self.image, (int(self.x), int(self.y)))

