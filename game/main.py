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
    """Display the about/credits screen."""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                waiting = False

        screen.fill((20, 40, 20))

        # Title
        title_text = font.render("URANEK REACTOR RUN", True, (150, 255, 150))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))



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

    # Draw room with corridors (pass boss_killed flag)
    room_manager.draw(screen, boss_killed)

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