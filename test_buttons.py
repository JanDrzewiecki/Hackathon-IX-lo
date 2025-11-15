import pygame
from pygame.locals import *

pygame.init()

# Load the start screen image
start_screen_image = pygame.image.load('game/ekran_startowy.png')
img_width, img_height = start_screen_image.get_size()

# Create fullscreen or use image size
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Button Position Test")

print(f"Screen size: {SCREEN_WIDTH} x {SCREEN_HEIGHT}")
print(f"Image size: {img_width} x {img_height}")

# Current button positions from main.py
start_button_rect = pygame.Rect(0, 0, 380, 80)
start_button_rect.center = (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 - 50)

about_button_rect = pygame.Rect(0, 0, 380, 80)
about_button_rect.center = (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 60)

exit_button_rect = pygame.Rect(0, 0, 380, 80)
exit_button_rect.center = (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 170)

print(f"\nCurrent button positions:")
print(f"START: center={start_button_rect.center}, rect={start_button_rect}")
print(f"ABOUT: center={about_button_rect.center}, rect={about_button_rect}")
print(f"EXIT: center={exit_button_rect.center}, rect={exit_button_rect}")

running = True
show_help = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        if event.type == MOUSEBUTTONDOWN:
            pos = event.pos
            print(f"Mouse clicked at: {pos}")
            if start_button_rect.collidepoint(pos):
                print("  -> START button hit!")
            elif about_button_rect.collidepoint(pos):
                print("  -> ABOUT button hit!")
            elif exit_button_rect.collidepoint(pos):
                print("  -> EXIT button hit!")
            else:
                print("  -> No button hit")
        if event.type == KEYDOWN and event.key == K_h:
            show_help = not show_help

    screen.fill((0, 0, 0))

    # Scale and draw the start screen
    scaled_start = pygame.transform.scale(start_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_start, (0, 0))

    # Draw button overlays
    pygame.draw.rect(screen, (255, 0, 0), start_button_rect, 3)
    pygame.draw.rect(screen, (0, 255, 0), about_button_rect, 3)
    pygame.draw.rect(screen, (0, 0, 255), exit_button_rect, 3)

    # Draw center points
    pygame.draw.circle(screen, (255, 255, 0), start_button_rect.center, 5)
    pygame.draw.circle(screen, (255, 255, 0), about_button_rect.center, 5)
    pygame.draw.circle(screen, (255, 255, 0), exit_button_rect.center, 5)

    # Draw labels
    font = pygame.font.SysFont("Arial", 20)

    start_label = font.render("START", True, (255, 255, 255))
    screen.blit(start_label, (start_button_rect.left + 10, start_button_rect.top - 30))

    about_label = font.render("ABOUT", True, (255, 255, 255))
    screen.blit(about_label, (about_button_rect.left + 10, about_button_rect.top - 30))

    exit_label = font.render("EXIT", True, (255, 255, 255))
    screen.blit(exit_label, (exit_button_rect.left + 10, exit_button_rect.top - 30))

    if show_help:
        help_font = pygame.font.SysFont("Arial", 16)
        help_text = [
            "Red box = START button",
            "Green box = ABOUT button",
            "Blue box = EXIT button",
            "Click anywhere to test detection",
            "Press ESC to exit",
            "Press H to toggle this help"
        ]
        y = 10
        for line in help_text:
            text = help_font.render(line, True, (255, 255, 255))
            bg_rect = pygame.Rect(5, y - 2, text.get_width() + 10, text.get_height() + 4)
            pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect)
            screen.blit(text, (10, y))
            y += 25

    pygame.display.update()

pygame.quit()
print("\nTest completed.")

