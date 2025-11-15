import pygame
from pygame.locals import *
from player import *
from enemy_spawner import *
from notification import *
from bullet import *
from settings import *
from room_manager import RoomManager
from hud import HeartsHUD
from blood_particles import BloodParticleSystem

pygame.init()

# Fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Hackaton Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri.ttf", 30)

# Load room background image
try:
    room_background = pygame.image.load("game/room-1.png").convert()
except:
    # If loading fails, try without 'game/' prefix
    try:
        room_background = pygame.image.load("room-1.png").convert()
    except:
        room_background = None
        print("Warning: Could not load room-1.png")

# Load map image
try:
    map_image = pygame.image.load("game/map.png").convert()
except:
    # If loading fails, try without 'game/' prefix
    try:
        map_image = pygame.image.load("map.png").convert()
    except:
        map_image = None
        print("Warning: Could not load map.png")

# Load start screen image
try:
    start_screen_image = pygame.image.load("game/ekran_startowy.png").convert()
except:
    # If loading fails, try without 'game/' prefix
    try:
        start_screen_image = pygame.image.load("ekran_startowy.png").convert()
    except:
        start_screen_image = None
        print("Warning: Could not load ekran_startowy.png")


def show_start_screen(screen, start_screen_image):
    """Display the start screen with interactive buttons.
    Returns 'start' to begin the game, 'about' for about screen, or 'quit' to exit."""
    if not start_screen_image:
        # If start screen image failed to load, skip this screen
        return 'start'

    # Define button positions based on the image layout
    # Buttons are positioned on the right side of the screen, lower area
    # START button (top button)
    start_button_rect = pygame.Rect(0, 0, 360, 90)
    start_button_rect.center = (SCREEN_WIDTH // 2 + 280, SCREEN_HEIGHT // 2 + 100)

    # ABOUT button (middle button)
    about_button_rect = pygame.Rect(0, 0, 360, 90)
    about_button_rect.center = (SCREEN_WIDTH // 2 + 280, SCREEN_HEIGHT // 2 + 270)

    # EXIT button (bottom button)
    exit_button_rect = pygame.Rect(0, 0, 360, 90)
    exit_button_rect.center = (SCREEN_WIDTH // 2 + 280, SCREEN_HEIGHT // 2 + 400)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return 'quit'
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if start_button_rect.collidepoint(mouse_pos):
                    return 'start'
                elif about_button_rect.collidepoint(mouse_pos):
                    return 'about'
                elif exit_button_rect.collidepoint(mouse_pos):
                    return 'quit'

        screen.fill((0, 0, 0))

        # Scale start screen to fit screen
        scaled_start = pygame.transform.scale(start_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_start, (0, 0))


        pygame.display.update()
        clock.tick(60)


def show_about_screen(screen, font):
    """Display the about/credits screen with pixel art theme."""
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
        for x in range(0, SCREEN_WIDTH, grid_size):
            pygame.draw.line(screen, grid_color, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(screen, grid_color, (0, y), (SCREEN_WIDTH, y), 1)

        # Animated scanline effect
        scanline_y = (animation_time * 5) % SCREEN_HEIGHT
        pygame.draw.rect(screen, (0, 255, 0, 50), (0, scanline_y, SCREEN_WIDTH, 3))

        # Draw pixel-style borders
        border_color = (0, 255, 0)
        border_width = 8
        pygame.draw.rect(screen, border_color, (border_width, border_width,
                                                SCREEN_WIDTH - border_width * 2,
                                                SCREEN_HEIGHT - border_width * 2), border_width)

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
            glow_rect = wow_glow.get_rect(center=(SCREEN_WIDTH // 2 + offset//2, y_offset + offset//2))
            screen.blit(wow_glow, glow_rect)

        # Main WOW text
        wow_text = large_font.render(wow_text_str, False, wow_colors[color_index])
        wow_rect = wow_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(wow_text, wow_rect)

        # Game title
        title_y = y_offset + 120
        title_text = medium_font.render("URANEK REACTOR RUN", True, (150, 255, 150))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, title_y))

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
            info_rect = info_render.get_rect(center=(SCREEN_WIDTH // 2, info_y + i * 45))

            # Pixel-style bracket decoration
            bracket_left = small_font.render("[", True, (0, 255, 0))
            bracket_right = small_font.render("]", True, (0, 255, 0))
            screen.blit(bracket_left, (info_rect.x - 30, info_rect.y))
            screen.blit(bracket_right, (info_rect.x + info_rect.width + 10, info_rect.y))
            screen.blit(info_render, info_rect)

        # Animated instruction at bottom
        instruction_y = SCREEN_HEIGHT - 80
        flash = (animation_time // 20) % 2
        if flash:
            instruction_text = small_font.render(">>> CLICK OR PRESS ANY KEY TO RETURN <<<", True, (0, 255, 0))
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, instruction_y))
            screen.blit(instruction_text, instruction_rect)

        # ESC hint
        esc_text = small_font.render("ESC - Back to Menu", True, (150, 150, 150))
        screen.blit(esc_text, (30, 30))

        animation_time += 1
        pygame.display.update()
        clock.tick(60)

    return 'start'



def show_map(screen, map_image):
    """Display the map image. Click anywhere or press any key to continue."""
    if not map_image:
        # If map image failed to load, skip this screen
        return

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                waiting = False

        screen.fill((0, 0, 0))

        # Scale map to fit screen
        scaled_map = pygame.transform.scale(map_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_map, (0, 0))

        # Add instruction text
        instruction_text = font.render("Click or press any key to start", True, (255, 255, 255))
        text_bg_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        text_bg_rect.inflate_ip(20, 10)
        pygame.draw.rect(screen, (0, 0, 0, 180), text_bg_rect, border_radius=8)
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT - 50 - instruction_text.get_height() // 2))

        pygame.display.update()
        clock.tick(60)


def start_new_game():
    """Reset all game state to start a fresh run."""
    global room_manager, player, enemies, level, enemy_spawner, notifications
    global bullets, bullets_cooldown, damage_cooldown, visited_rooms, cleared_rooms, hud, blood_systems

    # Create room manager with corridors
    room_manager = RoomManager(SCREEN_WIDTH, SCREEN_HEIGHT, margin_pixels=100)

    # Create player in center of game area
    player_start_x = room_manager.room_x + room_manager.room_width // 2 - URANEK_FRAME_WIDTH // 2
    player_start_y = room_manager.room_y + room_manager.room_height // 2 - URANEK_FRAME_WIDTH // 2
    player = Player(player_start_x, player_start_y)

    # Reset dynamic game state
    enemies = []
    level = 1
    enemy_spawner = EnemySpawner(level, room_manager)
    notifications = []
    bullets = []
    bullets_cooldown = 0
    damage_cooldown = 0
    blood_systems = []

    # Rooms progress
    visited_rooms = {0}
    cleared_rooms = set()

    # HUD
    hud = HeartsHUD()



def show_game_over(screen, font):
    gameover_img = None
    try:
        gameover_img = pygame.image.load("game/gameover.png").convert_alpha()
    except Exception:
        try:
            gameover_img = pygame.image.load("gameover.png").convert_alpha()
        except Exception:
            gameover_img = None

    if gameover_img is not None:
        img = pygame.transform.smoothscale(gameover_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        img_rect = img.get_rect(topleft=(0, 0))
    else:
        img = None
        img_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

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
        target_h = int(SCREEN_HEIGHT * 0.18)
        max_w = int(SCREEN_WIDTH * 0.45)
        scale = min(target_h / raw_h, max_w / raw_w)
        new_w = max(1, int(raw_w * scale))
        new_h = max(1, int(raw_h * scale))
        button_img = pygame.transform.smoothscale(button_img_raw, (new_w, new_h))
        button_rect = button_img.get_rect()
    else:
        button_img = None
        button_rect = pygame.Rect(0, 0, 360, 110)

    button_rect.centerx = SCREEN_WIDTH // 2
    button_rect.centery = int(SCREEN_HEIGHT * 0.85)

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
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            alpha = int(180 * progress)
            overlay.fill((0, 0, 0, alpha))
            screen.blit(overlay, (0, 0))
            if progress >= 1.0:
                return 'restart'

        pygame.display.update()
        clock.tick(60)


# Initial game state - Show start screen first
running = True
game_started = False

while running and not game_started:
    action = show_start_screen(screen, start_screen_image)
    if action == 'start':
        show_map(screen, map_image)
        start_new_game()
        game_started = True
    elif action == 'about':
        result = show_about_screen(screen, font)
        if result == 'quit':
            running = False
        # Otherwise loop back to start screen
    elif action == 'quit':
        running = False

while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    if room_background:
        scaled_bg = pygame.transform.scale(room_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))

    room_manager.draw(screen)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
    keys = pygame.key.get_pressed()


    # SHOOTING
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        mx, my = pygame.mouse.get_pos()
        if bullets_cooldown <= 0:
            bullets.append(Bullet(player, mx, my))
            bullets_cooldown = FPS / 3

    did_teleport = player.update(keys, room_manager)


    # Handle room transition
    if did_teleport:
        # Mark new room as visited
        visited_rooms.add(room_manager.current_room_id)
        # Clear enemies when changing rooms
        enemies.clear()
        # Reset enemy spawner for new room's enemy type (only if room not cleared)
        if room_manager.current_room_id not in cleared_rooms:
            enemy_spawner.reset_for_new_room()
        else:
            # Room is cleared, don't spawn enemies
            enemy_spawner.enemies_spawned_in_room = enemy_spawner.max_enemies_for_room
        # Add notifications
        notifications.append(
            Notification(player.x, player.y, "New Room!", "cyan", font)
        )
        # Add notification showing room number
        notifications.append(Notification(player.x, player.y, f"Room {room_manager.current_room_id}", "cyan", font))


    # Spawn enemies only if room is not cleared
    if room_manager.current_room_id not in cleared_rooms:
        enemy_spawner.update(enemies)

    # Check if room is now cleared (all enemies killed)
    if room_manager.current_room_id not in cleared_rooms and enemy_spawner.enemies_spawned_in_room >= enemy_spawner.max_enemies_for_room and len(enemies) == 0:
        cleared_rooms.add(room_manager.current_room_id)
        notifications.append(Notification(player.x, player.y, "Room Cleared!", "green", font))


    for enemy in enemies:
        enemy.update(player.x, player.y)
        enemy.draw(screen)
        if damage_cooldown <= 0 and player.hit_box.collide(enemy.hit_box):
            player.hp = max(0, player.hp - enemy.ad)
            damage_cooldown = int(FPS * 0.75)

    for notification in notifications:
        notification.update(notifications)
        notification.draw(screen)

    for bullet in bullets:
        bullet.update(bullets)
        bullet.draw(screen)

    # Update and draw blood particle systems
    for blood_system in blood_systems[:]:
        blood_system.update()
        blood_system.draw(screen)
        # Remove dead particle systems
        if not blood_system.is_alive():
            blood_systems.remove(blood_system)

    bullets_cooldown -= 1
    damage_cooldown = max(0, damage_cooldown - 1)
    for bullet in bullets[:]:
        if bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
            bullets.remove(bullet)


    # Draw HUD (hearts)
    hud.draw(screen, player)

    # Display current room and visited rooms in TOP-RIGHT corner
    room_text = font.render(f"Room: {room_manager.current_room_id}", True, (255, 255, 255))
    screen.blit(room_text, (SCREEN_WIDTH - room_text.get_width() - 20, 20))

    visited_text = font.render(f"Visited: {sorted(visited_rooms)}", True, (200, 200, 200))
    screen.blit(visited_text, (SCREEN_WIDTH - visited_text.get_width() - 20, 60))

    # Display cleared rooms
    if cleared_rooms:
        cleared_text = font.render(f"Cleared: {sorted(cleared_rooms)}", True, (100, 255, 100))
        screen.blit(cleared_text, (SCREEN_WIDTH - cleared_text.get_width() - 20, 100))

    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.hit_box.collide(enemy.hit_box):
                enemy.hp -= bullet.ad
                if enemy.hp <= 0:
                    # Create green blood particle explosion
                    blood_systems.append(BloodParticleSystem(enemy.x, enemy.y, num_particles=25))
                    enemies.remove(enemy)
                    player.points += 1
                bullets.remove(bullet)
                break

    player.draw(screen)

    if player.hp <= 0:
        # Show Game Over and decide next action
        action = show_game_over(screen, font)
        if action == 'quit':
            break
        elif action == 'restart':
            start_new_game()
            continue

    pygame.display.update()

pygame.quit()