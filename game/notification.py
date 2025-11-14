import pygame
import math
from settings import*

class Notification:

    def __init__(self, x, y, value, color, font):
        self.x = x
        self.y = y
        self.start_y = y
        self.value = value
        self.color = color
        self.timer = FPS * 2
        self.count = 0
        self.step = FPS
        self.font = font
        self.scale = 0.5  # Start small
        self.rotation = 0
        self.alpha = 255

    def draw(self, screen):
        # Calculate animation progress (0 to 1)
        progress = self.count / self.timer

        # Pulsating scale effect - starts small, grows, then shrinks
        if progress < 0.3:
            # Grow phase
            self.scale = 0.5 + (progress / 0.3) * 1.5  # From 0.5 to 2.0
        elif progress < 0.7:
            # Stay large
            self.scale = 2.0 + math.sin((progress - 0.3) * 10) * 0.2  # Slight pulse
        else:
            # Shrink phase
            self.scale = 2.0 - ((progress - 0.7) / 0.3) * 1.5  # From 2.0 to 0.5

        # Color animation - cycle through rainbow effect for gold
        if self.color == "gold":
            hue_shift = int(progress * 60)  # Cycle through colors
            r = 255
            g = min(255, 215 + int(math.sin(progress * 10) * 40))
            b = int(math.sin(progress * 15) * 100)
            current_color = (r, g, b)
        else:
            current_color = self.color

        # Fade out at the end
        if progress > 0.8:
            self.alpha = int(255 * (1 - (progress - 0.8) / 0.2))

        # Create text with special formatting for numbers
        if isinstance(self.value, int) or (isinstance(self.value, str) and self.value.isdigit()):
            display_text = f"+{self.value} ✨"  # Add sparkle emoji
        else:
            display_text = str(self.value)

        # Render text
        text = self.font.render(display_text, True, current_color)

        # Apply scaling
        scaled_width = int(text.get_width() * self.scale)
        scaled_height = int(text.get_height() * self.scale)

        if scaled_width > 0 and scaled_height > 0:
            scaled_text = pygame.transform.scale(text, (scaled_width, scaled_height))

            # Apply alpha transparency
            scaled_text.set_alpha(self.alpha)

            # Draw with glow effect for numbers
            if isinstance(self.value, int) or (isinstance(self.value, str) and self.value.isdigit()):
                # Draw glow layers
                glow_surface = pygame.Surface((scaled_width + 20, scaled_height + 20), pygame.SRCALPHA)
                for i in range(3):
                    glow_size = (scaled_width + i * 8, scaled_height + i * 8)
                    glow_alpha = int(self.alpha * 0.3 / (i + 1))
                    glow_text = pygame.transform.scale(text, glow_size)
                    glow_text.set_alpha(glow_alpha)
                    glow_text_rect = glow_text.get_rect(center=(scaled_width // 2 + 10, scaled_height // 2 + 10))
                    glow_surface.blit(glow_text, glow_text_rect)

                # Draw glow
                screen.blit(glow_surface, (self.x - 10, self.y - 10))

            # Draw main text centered
            text_rect = scaled_text.get_rect(center=(self.x + scaled_width // 2, self.y + scaled_height // 2))
            screen.blit(scaled_text, text_rect)

    def update(self, notifications: list["Notification"]):
        self.count += 1

        # Smooth floating movement
        progress = self.count / self.timer
        if progress < 0.5:
            # Float up
            self.y = self.start_y - int(progress * 100)
        else:
            # Slow down and start falling
            self.y = self.start_y - 50 + int((progress - 0.5) * 30)

        # Add slight horizontal wave motion
        self.x = self.x + math.sin(self.count * 0.3) * 0.5

        # Remove when timer expires
        if self.count >= self.timer:
            notifications.remove(self)
