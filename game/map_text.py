"""
Simple class to display pixel text on the map
"""
import pygame


class MapText:
    """Displays pixel text on the map image"""

    def __init__(self, text, position, font_size=40, color=(255, 255, 255)):
        """
        Initialize map text

        Args:
            text: The text to display
            position: (x, y) tuple for text position on the map
            font_size: Size of the font
            color: RGB color tuple for the text
        """
        self.text = text
        self.position = position
        self.font_size = font_size
        self.color = color

        # Create a pixel-style font (use None for default pygame font which is pixelated)
        self.font = pygame.font.Font(None, font_size)
        self.last_rect = None  # Store the last drawn rect for click detection

    def draw(self, surface, scale_factor=1.0, offset=(0, 0)):
        """
        Draw the text on the given surface

        Args:
            surface: pygame Surface to draw on
            scale_factor: Scale factor if the map is scaled
            offset: (x, y) offset for drawing position
        """
        # Scale position based on scale factor
        scaled_x = int(self.position[0] * scale_factor + offset[0])
        scaled_y = int(self.position[1] * scale_factor + offset[1])

        # Scale font size if needed
        scaled_font_size = max(1, int(self.font_size * scale_factor))
        scaled_font = pygame.font.Font(None, scaled_font_size)

        # Draw glow layers for radioactive effect (green glow)
        for offset_size in range(8, 0, -2):
            glow_color = (0, 255 - offset_size * 20, 0)
            glow_surf = scaled_font.render(self.text, False, glow_color)  # False = no antialiasing (pixel perfect)
            glow_rect = glow_surf.get_rect(center=(scaled_x + offset_size//2, scaled_y + offset_size//2))
            surface.blit(glow_surf, glow_rect)

        # Render text with dark outline for better visibility
        # Draw outline (dark green/black)
        outline_color = (0, 50, 0)
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2), (-2, 0), (2, 0), (0, -2), (0, 2)]:
            outline_surf = scaled_font.render(self.text, False, outline_color)  # False = no antialiasing (pixel perfect)
            outline_rect = outline_surf.get_rect(center=(scaled_x + dx, scaled_y + dy))
            surface.blit(outline_surf, outline_rect)

        # Draw main text - PIXEL PERFECT (no antialiasing)
        text_surf = scaled_font.render(self.text, False, self.color)  # False = no antialiasing (pixel perfect)
        text_rect = text_surf.get_rect(center=(scaled_x, scaled_y))
        surface.blit(text_surf, text_rect)

        # Store the rect for click detection
        self.last_rect = text_rect

        return text_rect

    def is_clicked(self, mouse_pos):
        """
        Check if the text was clicked

        Args:
            mouse_pos: (x, y) tuple of mouse position

        Returns:
            True if the text was clicked, False otherwise
        """
        if self.last_rect is None:
            return False
        return self.last_rect.collidepoint(mouse_pos)


class EuroAsiaMapText(MapText):
    """Specific class for EURO-ASIA text on map.png"""

    def __init__(self):
        """Initialize EURO-ASIA text positioned over Eurasia on the map"""
        # Position approximately over Eurasia (adjust based on your map.png dimensions)
        # Assuming map is roughly 1200x800, Eurasia is around the center-right
        eurasia_x = 1050  # Adjust this based on your map
        eurasia_y = 400  # Adjust this based on your map

        super().__init__(
            text="EURO-ASIA",
            position=(eurasia_x, eurasia_y),
            font_size=48,
            color=(0, 255, 0)  # Bright radioactive green
        )


class NorthSouthAmericaMapText(MapText):
    """Specific class for NORTH AND SOUTH AMERICA text on map2.png"""

    def __init__(self):
        """Initialize NORTH AND SOUTH AMERICA text positioned over the Americas on the map"""
        # Position approximately over North/South America (left side of map)
        # Assuming map is roughly 1200x800, Americas are on the left side
        americas_x = 445  # Adjusted: moved 75 pixels right (370 + 75)
        americas_y = 620  # Keep Y position same

        super().__init__(
            text="NORTH AND SOUTH AMERICA",
            position=(americas_x, americas_y),
            font_size=25,  # Slightly smaller to fit the longer text
            color=(0, 255, 0)  # Bright radioactive green
        )


class AfricaMapText(MapText):
    """Specific class for AFRICA text on map.png for level 2"""

    def __init__(self):
        """Initialize AFRICA text positioned in the center of the map"""
        # Position in center of map
        # Assuming map is roughly 1200x800
        africa_x = 850  # Adjusted: moved 50 pixels right (800 + 50)
        africa_y = 600  # Adjusted: moved 100 pixels up (700 - 100)

        super().__init__(
            text="AFRICA",
            position=(africa_x, africa_y),
            font_size=60,  # Large font for dramatic effect
            color=(0, 255, 0)  # Bright radioactive green
        )
