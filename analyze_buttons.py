import pygame
import sys

pygame.init()

# Load the start screen image
try:
    img = pygame.image.load('game/ekran_startowy.png')
    print(f"Image loaded successfully!")
    print(f"Image size: {img.get_size()}")

    # Create a display window
    screen = pygame.display.set_mode(img.get_size())
    pygame.display.set_caption("Click on button centers - START, ABOUT, EXIT")

    # Store button clicks
    clicks = []
    button_names = ["START", "ABOUT", "EXIT"]

    running = True
    while running and len(clicks) < 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                clicks.append(pos)
                print(f"{button_names[len(clicks)-1]} button center: {pos}")
                if len(clicks) >= 3:
                    running = False

        # Draw the image
        screen.blit(img, (0, 0))

        # Draw clicked points
        for i, click in enumerate(clicks):
            pygame.draw.circle(screen, (255, 0, 0), click, 5)
            font = pygame.font.SysFont("Arial", 20)
            text = font.render(button_names[i], True, (255, 255, 0))
            screen.blit(text, (click[0] + 10, click[1] - 10))

        # Draw instruction
        font = pygame.font.SysFont("Arial", 16)
        if len(clicks) < 3:
            text = font.render(f"Click center of {button_names[len(clicks)]} button", True, (255, 255, 255))
            pygame.draw.rect(screen, (0, 0, 0), (10, 10, text.get_width() + 10, text.get_height() + 10))
            screen.blit(text, (15, 15))

        pygame.display.flip()

    if len(clicks) == 3:
        print("\n=== Button Configuration ===")
        print(f"Image size: {img.get_size()}")
        for i, (name, pos) in enumerate(zip(button_names, clicks)):
            print(f"{name}: center=({pos[0]}, {pos[1]})")

    pygame.quit()

except Exception as e:
    print(f"Error: {e}")
    pygame.quit()

