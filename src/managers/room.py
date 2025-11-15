import pygame
from src.core.constants import *


class Room:
    def __init__(self, screen_width, screen_height, margin_pixels=200):
        """
        Create a room with specified margin from screen edges.

        Args:
            screen_width: Width of the screen
            screen_height: Height of the screen
            margin_pixels: Margin from screen edges in pixels (default 200px)
        """

        # Calculate room size based on screen size minus margins on all sides
        self.width = screen_width - (2 * margin_pixels)
        self.height = screen_height - (2 * margin_pixels)
        print(self.height, self.width)

        # Position the room with exact margin from edges
        self.x = margin_pixels
        self.y = margin_pixels

        # Colors
        self.bg_color = (50, 50, 50)  # Dark gray background
        self.border_color = (255, 255, 255)  # White border
        self.border_width = 3

    def draw(self, screen):
        """Draw the room on the screen."""
        # Draw background
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.width, self.height))
        # Draw border
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), self.border_width)

    def get_bounds(self):
        """Return the room boundaries (x, y, width, height)."""
        return self.x, self.y, self.width, self.height

    def get_random_spawn_position(self):
        """Get a random position on one of the room edges for enemy spawning."""
        import random

        # Choose random edge: 0=top, 1=bottom, 2=left, 3=right
        edge = random.randint(0, 3)

        if edge == 0:  # Top edge
            x = random.randint(self.x, self.x + self.width - ENEMY_SIZE)
            y = self.y
        elif edge == 1:  # Bottom edge
            x = random.randint(self.x, self.x + self.width - ENEMY_SIZE)
            y = self.y + self.height - ENEMY_SIZE
        elif edge == 2:  # Left edge
            x = self.x
            y = random.randint(self.y, self.y + self.height - ENEMY_SIZE)
        else:  # Right edge
            x = self.x + self.width - ENEMY_SIZE
            y = random.randint(self.y, self.y + self.height - ENEMY_SIZE)

        return x, y

    def is_inside(self, x, y, object_size):
        """Check if an object is inside the room bounds."""
        return (self.x <= x and
                x + object_size <= self.x + self.width and
                self.y <= y and
                y + object_size <= self.y + self.height)

    def clamp_position(self, x, y, object_size):
        """Clamp position to keep object inside the room."""
        x = max(self.x, min(x, self.x + self.width - object_size))
        y = max(self.y, min(y, self.y + self.height - object_size))
        return x, y

