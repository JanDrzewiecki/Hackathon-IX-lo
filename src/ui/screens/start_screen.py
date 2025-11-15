"""
Start screen with interactive buttons and click animations.
"""
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN


def show_start_screen(screen, start_screen_image, clock, screen_width, screen_height):
    """
    Display the start screen with interactive buttons and a simple click animation.
    
    Args:
        screen: pygame screen surface
        start_screen_image: loaded start screen image
        clock: pygame clock for FPS control
        screen_width: screen width in pixels
        screen_height: screen height in pixels
        
    Returns:
        'start' to begin the game, 'about' for about screen, or 'quit' to exit
    """
    if not start_screen_image:
        # If start screen image failed to load, skip this screen
        return 'start'

    # Buttons layout on the right side of the screen
    start_button_rect = pygame.Rect(0, 0, 360, 90)
    start_button_rect.center = (screen_width // 2 + 280, screen_height // 2 + 100)

    about_button_rect = pygame.Rect(0, 0, 360, 90)
    about_button_rect.center = (screen_width // 2 + 280, screen_height // 2 + 270)

    exit_button_rect = pygame.Rect(0, 0, 360, 90)
    exit_button_rect.center = (screen_width // 2 + 280, screen_height // 2 + 400)

    # Click animation state
    click_action = None  # 'start' | 'about' | 'quit'
    click_pos = None     # (x, y)
    click_start_ms = 0
    click_duration_ms = 420

    def ease_out_cubic(t: float) -> float:
        t = max(0.0, min(1.0, t))
        return 1 - (1 - t) ** 3

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return 'quit'
            if click_action is None and event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if start_button_rect.collidepoint(mouse_pos):
                    click_action = 'start'
                    click_pos = mouse_pos
                    click_start_ms = pygame.time.get_ticks()
                elif about_button_rect.collidepoint(mouse_pos):
                    click_action = 'about'
                    click_pos = mouse_pos
                    click_start_ms = pygame.time.get_ticks()
                elif exit_button_rect.collidepoint(mouse_pos):
                    click_action = 'quit'
                    click_pos = mouse_pos
                    click_start_ms = pygame.time.get_ticks()

        screen.fill((0, 0, 0))

        # Scale start screen to fit screen
        scaled_start = pygame.transform.scale(start_screen_image, (screen_width, screen_height))
        screen.blit(scaled_start, (0, 0))

        # If clicked, play a zoom-and-tilt animation (no circle) and then finish
        if click_action is not None:
            elapsed = pygame.time.get_ticks() - click_start_ms
            t = min(1.0, elapsed / click_duration_ms)
            et = ease_out_cubic(t)

            # Camera-like gentle zoom-in with slight tilt
            zoom = 1.0 + 0.12 * et  # up to ~12% zoom
            angle = (1.0 - (abs((hash(click_action) % 7) - 3) / 3.0)) * 4.0  # small deterministic angle per action
            angle *= (0.5 + 0.5 * et)  # ramp up rotation a bit

            zoomed = pygame.transform.rotozoom(scaled_start, angle, zoom)
            zr = zoomed.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(zoomed, zr.topleft)

            # Slight dark fade of the whole screen during animation
            fade_alpha = int(160 * t)
            fade = pygame.Surface((screen_width, screen_height))
            fade.set_alpha(fade_alpha)
            fade.fill((0, 0, 0))
            screen.blit(fade, (0, 0))

            if elapsed >= click_duration_ms:
                return click_action

        pygame.display.update()
        clock.tick(60)
