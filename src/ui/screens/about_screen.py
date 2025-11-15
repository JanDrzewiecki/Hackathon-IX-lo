"""
About/credits screen with pixel art theme.
"""
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN


def show_about_screen(screen, font, clock, screen_width, screen_height):
    """
    Display the about/credits screen with pixel art theme.
    
    Args:
        screen: pygame screen surface
        font: pygame font for text rendering
        clock: pygame clock for FPS control
        screen_width: screen width in pixels
        screen_height: screen height in pixels
        
    Returns:
        'start' to return to start screen, 'quit' to exit
    """
    # Create larger fonts for the WOW text
    large_font = pygame.font.Font(None, 150)
    medium_font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 35)

    waiting = True
    # Animation variables
    animation_time = 0

    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 'start'
                else:
                    waiting = False
            if event.type == MOUSEBUTTONDOWN:
                waiting = False

        # Dark green/radioactive background with pixel grid effect
        screen.fill((15, 25, 15))

        # Draw pixel grid pattern
        grid_color = (25, 45, 25)
        grid_size = 20
        for x in range(0, screen_width, grid_size):
            pygame.draw.line(screen, grid_color, (x, 0), (x, screen_height), 1)
        for y in range(0, screen_height, grid_size):
            pygame.draw.line(screen, grid_color, (0, y), (screen_width, y), 1)

        # Animated scanline effect
        scanline_y = (animation_time * 5) % screen_height
        pygame.draw.rect(screen, (0, 255, 0, 50), (0, scanline_y, screen_width, 3))

        # Draw pixel-style borders
        border_color = (0, 255, 0)
        border_width = 8
        pygame.draw.rect(screen, border_color, (border_width, border_width,
                                                screen_width - border_width * 2,
                                                screen_height - border_width * 2), border_width)

        # Animated WOW text with glowing effect
        y_offset = 150
        wow_colors = [
            (0, 255, 0),      # Bright green
            (50, 255, 50),    # Light green
            (100, 255, 100)   # Even lighter
        ]

        # Draw WOW with shadow/glow effect
        wow_text_str = "WOW!"
        color_index = (animation_time // 10) % len(wow_colors)

        # Glow layers
        for offset in range(8, 0, -2):
            glow_color = (0, 255 - offset * 20, 0)
            wow_glow = large_font.render(wow_text_str, False, glow_color)
            glow_rect = wow_glow.get_rect(center=(screen_width // 2 + offset//2, y_offset + offset//2))
            screen.blit(wow_glow, glow_rect)

        # Main WOW text
        wow_text = large_font.render(wow_text_str, False, wow_colors[color_index])
        wow_rect = wow_text.get_rect(center=(screen_width // 2, y_offset))
        screen.blit(wow_text, wow_rect)

        # Game title
        title_y = y_offset + 120
        title_text = medium_font.render("URANEK REACTOR RUN", True, (150, 255, 150))
        title_rect = title_text.get_rect(center=(screen_width // 2, title_y))

        # Title background box
        box_padding = 20
        title_box = pygame.Rect(title_rect.x - box_padding, title_rect.y - box_padding//2,
                               title_rect.width + box_padding * 2, title_rect.height + box_padding)
        pygame.draw.rect(screen, (0, 50, 0), title_box)
        pygame.draw.rect(screen, (0, 200, 0), title_box, 3)
        screen.blit(title_text, title_rect)

        # Credits/Info in pixel style boxes
        info_y = title_y + 100
        info_texts = [
            "Written by:",
            " - Jan Drzewiecki",
            " - Wiktor Owerczuk",
            " - Witold Cieslinski",
            "Designed by:",
            " - Lukasz Ciskowski"
        ]

        for i, text in enumerate(info_texts):
            # Alternating colors for pixel aesthetic
            text_color = (100, 255, 100) if i % 2 == 0 else (150, 255, 150)
            info_render = small_font.render(text, True, text_color)
            info_rect = info_render.get_rect(center=(screen_width // 2, info_y + i * 45))

            # Pixel-style bracket decoration
            bracket_left = small_font.render("[", True, (0, 255, 0))
            bracket_right = small_font.render("]", True, (0, 255, 0))
            screen.blit(bracket_left, (info_rect.x - 30, info_rect.y))
            screen.blit(bracket_right, (info_rect.x + info_rect.width + 10, info_rect.y))
            screen.blit(info_render, info_rect)

        # Animated instruction at bottom
        instruction_y = screen_height - 80
        flash = (animation_time // 20) % 2
        if flash:
            instruction_text = small_font.render(">>> CLICK OR PRESS ANY KEY TO RETURN <<<", True, (0, 255, 0))
            instruction_rect = instruction_text.get_rect(center=(screen_width // 2, instruction_y))
            screen.blit(instruction_text, instruction_rect)

        # ESC hint
        esc_text = small_font.render("ESC - Back to Menu", True, (150, 150, 150))
        screen.blit(esc_text, (30, 30))

        animation_time += 1
        pygame.display.update()
        clock.tick(60)

    return 'start'
