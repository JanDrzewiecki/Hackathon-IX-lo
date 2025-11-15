import pygame
from pygame.locals import *
from player import *
from enemy_spawner import *
from notification import *
from bullet import *
from enemy_bullet import EnemyBullet
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
    """Display the start screen with interactive buttons and a simple click animation.
    Returns 'start' to begin the game, 'about' for about screen, or 'quit' to exit."""
    if not start_screen_image:
        # If start screen image failed to load, skip this screen
        return 'start'

    # Buttons layout on the right side of the screen
    start_button_rect = pygame.Rect(0, 0, 360, 90)
    start_button_rect.center = (SCREEN_WIDTH // 2 + 280, SCREEN_HEIGHT // 2 + 100)

    about_button_rect = pygame.Rect(0, 0, 360, 90)
    about_button_rect.center = (SCREEN_WIDTH // 2 + 280, SCREEN_HEIGHT // 2 + 270)

    exit_button_rect = pygame.Rect(0, 0, 360, 90)
    exit_button_rect.center = (SCREEN_WIDTH // 2 + 280, SCREEN_HEIGHT // 2 + 400)

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
        scaled_start = pygame.transform.scale(start_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_start, (0, 0))

        # No hover outline for buttons (as requested)

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
            zr = zoomed.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(zoomed, zr.topleft)

            # Slight dark fade of the whole screen during animation
            fade_alpha = int(160 * t)
            fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade.set_alpha(fade_alpha)
            fade.fill((0, 0, 0))
            screen.blit(fade, (0, 0))

            if elapsed >= click_duration_ms:
                return click_action

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
    """Display the map image. Click to zoom into the clicked point with a short animation."""
    if not map_image:
        # If map image failed to load, skip this screen
        return

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
            if not animating and event.type == KEYDOWN:
                # Allow skipping the map with any key if no animation has started
                return
            if not animating and event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Start zoom-in animation toward the clicked point
                click_pos = event.pos
                anim_start_ms = pygame.time.get_ticks()
                animating = True

        screen.fill((0, 0, 0))

        # Base map scaled to screen size
        base_map = pygame.transform.scale(map_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        if animating and click_pos is not None:
            elapsed = pygame.time.get_ticks() - anim_start_ms
            t = min(1.0, elapsed / anim_duration_ms)
            et = ease_out_cubic(t)

            # Zoom from 1.0 to ~1.8x with easing
            zoom = 1.0 + 0.8 * et
            zw = max(1, int(SCREEN_WIDTH * zoom))
            zh = max(1, int(SCREEN_HEIGHT * zoom))
            zoomed = pygame.transform.smoothscale(base_map, (zw, zh))

            # Pan so that the clicked point moves toward the center during zoom
            cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            tlx = int(cx - click_pos[0] * zoom)
            tly = int(cy - click_pos[1] * zoom)
            screen.blit(zoomed, (tlx, tly))

            # Subtle dark overlay during the animation
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, int(150 * t)))
            screen.blit(overlay, (0, 0))

            if t >= 1.0:
                # Finish after the animation completes
                return
        else:
            # Idle (before click) view with instruction
            screen.blit(base_map, (0, 0))
            instruction_text = font.render("Kliknij w mapę, aby przybliżyć i rozpocząć", True, (255, 255, 255))
            text_bg_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            text_bg_rect.inflate_ip(20, 10)
            # Semi-transparent background for better readability
            bg = pygame.Surface((text_bg_rect.width, text_bg_rect.height), pygame.SRCALPHA)
            bg.fill((0, 0, 0, 180))
            screen.blit(bg, text_bg_rect.topleft)
            screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2,
                                           SCREEN_HEIGHT - 50 - instruction_text.get_height() // 2))

        pygame.display.update()
        clock.tick(60)


def start_new_game():
    """Reset all game state to start a fresh run."""
    global room_manager, player, enemies, level, enemy_spawner, notifications
    global bullets, enemy_bullets, bullets_cooldown, damage_cooldown, visited_rooms, cleared_rooms, hud, blood_systems, boss_killed, current_level

    # Create room manager with corridors
    room_manager = RoomManager(SCREEN_WIDTH, SCREEN_HEIGHT, margin_pixels=100)

    # Create player in center of game area
    player_start_x = room_manager.room_x + room_manager.room_width // 2 - URANEK_FRAME_WIDTH // 2
    player_start_y = room_manager.room_y + room_manager.room_height // 2 - URANEK_FRAME_WIDTH // 2
    player = Player(player_start_x, player_start_y)

    # Initialize all game state variables
    enemies = []
    level = 1
    enemy_spawner = EnemySpawner(level, room_manager)
    notifications = []
    bullets = []
    enemy_bullets = []
    bullets_cooldown = 0
    damage_cooldown = 0
    blood_systems = []
    visited_rooms = {0}
    cleared_rooms = set()
    boss_killed = False
    current_level = 1
    hud = HeartsHUD()


# Initialize global variables as None before game starts
room_manager = None
player = None
enemies = []
level = 1
enemy_spawner = None
notifications = []
bullets = []
enemy_bullets = []
bullets_cooldown = 0
damage_cooldown = 0
blood_systems = []
visited_rooms = {0}
cleared_rooms = set()
boss_killed = False
current_level = 1
hud = None



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

    # Draw room background image if loaded
    if room_background:
        # Scale image to fit screen
        scaled_bg = pygame.transform.scale(room_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))

    # Check if current room is cleared
    room_cleared = room_manager.current_room_id in cleared_rooms

    # Update door animation
    room_manager.update_door_animation(room_cleared)

    # Draw room with corridors (doors close behind you until you clear the room)
    room_manager.draw(screen, boss_killed, room_cleared)

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

    did_teleport = player.update(keys, room_manager, visited_rooms, enemies, boss_killed)

    # Handle special corridor (NEXT LEVEL after boss)
    if did_teleport == "next_level":
        # Player reached the NEXT LEVEL corridor - show map
        show_map(screen, map_image)
        # After map, restart game or continue
        start_new_game()
        continue

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
        # Add notification showing room number
        notifications.append(Notification(player.x, player.y, f"Room {room_manager.current_room_id}", "cyan", font))


    # Spawn enemies only if room is not cleared
    if room_manager.current_room_id not in cleared_rooms:
        enemy_spawner.update(enemies)

    # Check if room is now cleared (all enemies killed)
    if room_manager.current_room_id not in cleared_rooms and enemy_spawner.enemies_spawned_in_room >= enemy_spawner.max_enemies_for_room and len(enemies) == 0:
        cleared_rooms.add(room_manager.current_room_id)

        # Check if boss room (room 5) was cleared
        if room_manager.current_room_id == 5:
            boss_killed = True
            notifications.append(Notification(player.x, player.y, "NASTĘPNY POZIOM!", "gold", font))
        else:
            notifications.append(Notification(player.x, player.y, "Room Cleared!", "green", font))


    for enemy in enemies:
        enemy.update(player.x, player.y, enemy_bullets)
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

    # Update and draw enemy bullets
    for eb in enemy_bullets[:]:
        eb.update()
        eb.draw(screen)
        # Remove if out of screen
        if eb.x < 0 or eb.x > SCREEN_WIDTH or eb.y < 0 or eb.y > SCREEN_HEIGHT:
            enemy_bullets.remove(eb)
        # Check collision with player
        elif damage_cooldown <= 0 and player.hit_box.collide(eb.hit_box):
            player.hp = max(0, player.hp - eb.ad)
            damage_cooldown = int(FPS * 0.75)
            enemy_bullets.remove(eb)

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

    # Display current level
    level_text = font.render(f"Level: {current_level}", True, (255, 215, 0))
    screen.blit(level_text, (20, 100))

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