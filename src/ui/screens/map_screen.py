"""
Map screen with zoom animation and clickable regions.
"""
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, K_p


def show_map(screen, map_image, font, clock, screen_width, screen_height, level_num=1, show_text=True, text_class=None):
    """
    Display the map image. Click on region text to start the game with zoom animation.

    Args:
        screen: pygame screen surface
        map_image: the map image to display
        font: pygame font for text rendering
        clock: pygame clock for FPS control
        screen_width: screen width in pixels
        screen_height: screen height in pixels
        level_num: current level number (for display)
        show_text: whether to show the region text (False for completed regions)
        text_class: MapText subclass to use (default: EuroAsiaMapText)
        
    Returns:
        None normally, or "skip_to_level_3" if P key pressed
    """
    from src.ui.map_text import EuroAsiaMapText
    
    if not map_image:
        # If map image failed to load, skip this screen
        return

    # Create text instance only if we should show it
    if text_class is None:
        text_class = EuroAsiaMapText

    region_text = text_class() if show_text else None

    # Animation state
    animating = False
    click_pos = None
    anim_start_ms = 0
    anim_duration_ms = 700

    def ease_out_cubic(t: float) -> float:
        t = max(0.0, min(1.0, t))
        return 1 - (1 - t) ** 3

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                # Only ESC to quit
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_p:
                # P key to skip to level 3 (for testing)
                return "skip_to_level_3"
            if not animating and event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # Only allow clicking if text exists AND was clicked
                if region_text is not None and region_text.is_clicked(mouse_pos):
                    # Start zoom animation toward clicked point
                    click_pos = mouse_pos
                    anim_start_ms = pygame.time.get_ticks()
                    animating = True
                # If text exists and clicked elsewhere, do nothing

        screen.fill((0, 0, 0))

        # Base map scaled to screen size
        base_map = pygame.transform.scale(map_image, (screen_width, screen_height))

        # Calculate scale factor from original map to screen size
        scale_x = screen_width / map_image.get_width()
        scale_y = screen_height / map_image.get_height()
        scale_factor = min(scale_x, scale_y)

        if animating and click_pos is not None:
            elapsed = pygame.time.get_ticks() - anim_start_ms
            t = min(1.0, elapsed / anim_duration_ms)
            et = ease_out_cubic(t)

            # Zoom from 1.0 to ~2.0x with easing
            zoom = 1.0 + 1.0 * et
            zw = max(1, int(screen_width * zoom))
            zh = max(1, int(screen_height * zoom))
            zoomed = pygame.transform.smoothscale(base_map, (zw, zh))

            # Pan so that the clicked point moves toward the center during zoom
            cx, cy = screen_width // 2, screen_height // 2
            tlx = int(cx - click_pos[0] * zoom)
            tly = int(cy - click_pos[1] * zoom)
            screen.blit(zoomed, (tlx, tly))

            # Subtle dark overlay during the animation
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, int(150 * t)))
            screen.blit(overlay, (0, 0))

            if t >= 1.0:
                # Finish after the animation completes
                return
        else:
            # Idle (before click) view with instruction
            screen.blit(base_map, (0, 0))

            # Draw region text on the map if it exists
            if region_text:
                region_text.draw(screen, scale_factor, (0, 0))
                # Show instruction for clicking on the region text
                instruction_text = font.render(f"Kliknij na {region_text.text}, aby rozpocząć", True, (255, 255, 255))
            else:
                # Show generic instruction when no text to click
                instruction_text = font.render("Kliknij w mapę, aby rozpocząć", True, (255, 255, 255))

            text_bg_rect = instruction_text.get_rect(center=(screen_width // 2, screen_height - 50))
            text_bg_rect.inflate_ip(20, 10)
            # Semi-transparent background for better readability
            bg = pygame.Surface((text_bg_rect.width, text_bg_rect.height), pygame.SRCALPHA)
            bg.fill((0, 0, 0, 180))
            screen.blit(bg, text_bg_rect.topleft)
            screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2,
                                           screen_height - 50 - instruction_text.get_height() // 2))

        pygame.display.update()
        clock.tick(60)
