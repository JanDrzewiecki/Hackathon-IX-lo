"""
Game over screen with play again button.
"""
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN


def show_game_over(screen, font, clock, screen_width, screen_height):
    """
    Display the game over screen with play again button.
    
    Args:
        screen: pygame screen surface
        font: pygame font for text rendering
        clock: pygame clock for FPS control
        screen_width: screen width in pixels
        screen_height: screen height in pixels
        
    Returns:
        'restart' to play again, 'quit' to exit
    """
    gameover_img = None
    try:
        gameover_img = pygame.image.load("game/gameover.png").convert_alpha()
    except Exception:
        try:
            gameover_img = pygame.image.load("gameover.png").convert_alpha()
        except Exception:
            gameover_img = None

    if gameover_img is not None:
        img = pygame.transform.smoothscale(gameover_img, (screen_width, screen_height))
        img_rect = img.get_rect(topleft=(0, 0))
    else:
        img = None
        img_rect = pygame.Rect(0, 0, screen_width, screen_height)

    button_img_raw = None
    try:
        button_img_raw = pygame.image.load("game/playagainbutton.png").convert_alpha()
    except Exception:
        try:
            button_img_raw = pygame.image.load("playagainbutton.png").convert_alpha()
        except Exception:
            button_img_raw = None

    if button_img_raw is not None:
        raw_w, raw_h = button_img_raw.get_size()
        target_h = int(screen_height * 0.18)
        max_w = int(screen_width * 0.45)
        scale = min(target_h / raw_h, max_w / raw_w)
        new_w = max(1, int(raw_w * scale))
        new_h = max(1, int(raw_h * scale))
        button_img = pygame.transform.smoothscale(button_img_raw, (new_w, new_h))
        button_rect = button_img.get_rect()
    else:
        button_img = None
        button_rect = pygame.Rect(0, 0, 360, 110)

    button_rect.centerx = screen_width // 2
    button_rect.centery = int(screen_height * 0.85)

    pressed = False
    press_start = 0
    press_duration_ms = 180

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return 'quit'
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos) and not pressed:
                    pressed = True
                    press_start = pygame.time.get_ticks()

        screen.fill((0, 0, 0))
        if img is not None:
            screen.blit(img, img_rect)

        hint_text = font.render("ESC - Quit", True, (200, 200, 200))
        screen.blit(hint_text, (20, 20))

        progress = 0.0
        if pressed:
            elapsed = pygame.time.get_ticks() - press_start
            progress = max(0.0, min(1.0, elapsed / press_duration_ms))

        scale_factor = 1.0 - 0.08 * progress

        if button_img is not None:
            if scale_factor != 1.0:
                new_w = max(1, int(button_img.get_width() * scale_factor))
                new_h = max(1, int(button_img.get_height() * scale_factor))
                scaled_btn = pygame.transform.smoothscale(button_img, (new_w, new_h))
                scaled_rect = scaled_btn.get_rect(center=button_rect.center)
                screen.blit(scaled_btn, scaled_rect.topleft)
            else:
                screen.blit(button_img, button_rect.topleft)
        else:
            hovered = button_rect.collidepoint(pygame.mouse.get_pos()) and not pressed
            base_color = (60, 140, 60)
            hover_color = (80, 180, 80)
            btn_color = hover_color if hovered else base_color
            draw_rect = button_rect.copy()
            if scale_factor != 1.0:
                draw_rect.width = max(1, int(draw_rect.width * scale_factor))
                draw_rect.height = max(1, int(draw_rect.height * scale_factor))
                draw_rect.center = button_rect.center
            pygame.draw.rect(screen, btn_color, draw_rect, border_radius=12)
            pygame.draw.rect(screen, (255, 255, 255), draw_rect, width=2, border_radius=12)
            btn_text = font.render("PLAY AGAIN", True, (255, 255, 255))
            screen.blit(btn_text, (draw_rect.centerx - btn_text.get_width() // 2,
                                   draw_rect.centery - btn_text.get_height() // 2))

        if progress > 0.0:
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            alpha = int(180 * progress)
            overlay.fill((0, 0, 0, alpha))
            screen.blit(overlay, (0, 0))

        if progress >= 1.0:
            return 'restart'

        pygame.display.update()
        clock.tick(60)
