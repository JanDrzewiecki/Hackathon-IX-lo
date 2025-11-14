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


def start_new_game():
    """Reset all game state to start a fresh run."""
    global room_manager, player, enemies, level, enemy_spawner, notifications
    global bullets, bullets_cooldown, damage_cooldown, visited_rooms, cleared_rooms, hud

    # Create room manager with corridors
    room_manager = RoomManager(SCREEN_WIDTH, SCREEN_HEIGHT, margin_pixels=100)

    # Create player in center of game area
    player_start_x = room_manager.room_x + room_manager.room_width // 2 - URANEK_FRAME_WIDTH // 2
    player_start_y = room_manager.room_y + room_manager.room_height // 2 - URANEK_FRAME_WIDTH // 2
    player = Player(player_start_x, player_start_y)

enemies = []
level = 1
enemy_spawner = EnemySpawner(level, room_manager)
notifications = []
bullets = []
bullets_cooldown = 0
damage_cooldown = 0
blood_systems = []  # List for blood particle systems

visited_rooms = {0}
cleared_rooms = set()

hud = HeartsHUD()


def show_game_over(screen, font):
    """Display Game Over screen with a PLAY AGAIN button.
    Returns 'restart' if the button was clicked, or 'quit' if ESC/quit is pressed.
    """
    button_rect = pygame.Rect(0, 0, 260, 70)
    button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return 'quit'
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    return 'restart'

        screen.fill((0, 0, 0))

        go_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, SCREEN_HEIGHT // 2 - 120))

        info_text = font.render("Press ESC to quit", True, (200, 200, 200))
        screen.blit(info_text, (SCREEN_WIDTH // 2 - info_text.get_width() // 2, SCREEN_HEIGHT // 2 - 70))

        # Hover effect color
        hovered = button_rect.collidepoint(pygame.mouse.get_pos())
        btn_color = (80, 180, 80) if hovered else (60, 140, 60)
        pygame.draw.rect(screen, btn_color, button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), button_rect, width=2, border_radius=12)

        btn_text = font.render("PLAY AGAIN", True, (255, 255, 255))
        screen.blit(btn_text, (button_rect.centerx - btn_text.get_width() // 2,
                               button_rect.centery - btn_text.get_height() // 2))

        pygame.display.update()
        clock.tick(60)


# Initial game state
start_new_game()

running = True

while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    # Draw room background image if loaded
    if room_background:
        # Scale image to fit screen
        scaled_bg = pygame.transform.scale(room_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))

    # Draw room with corridors
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

    # DEBUG: Print player position after update if keys were pressed
    if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
        print(f"After move: ({player.x:.1f}, {player.y:.1f})")

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