import pygame
from pygame.locals import *
from player import *
from enemy_spawner import *
from notification import *
from bullet import *
from settings import *
from room_manager import RoomManager
from hud import HeartsHUD

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

# Track visited rooms
visited_rooms = {0}  # Start room is visited

hud = HeartsHUD()

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

    # DEBUG: Print player position when keys are pressed
    if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
        old_x, old_y = player.x, player.y
        print(f"Before move: ({old_x:.1f}, {old_y:.1f})", end=" -> ")

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
        # Reset enemy spawner for new room's enemy type
        enemy_spawner.reset_for_new_room()
        # Add notifications
        notifications.append(
            Notification(player.x, player.y, "New Room!", "cyan", font)
        )
        # Add notification showing room number
        notifications.append(Notification(player.x, player.y, f"Room {room_manager.current_room_id}", "cyan", font))


    enemy_spawner.update(enemies)


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

    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.hit_box.collide(enemy.hit_box):
                enemy.hp -= bullet.ad
                if enemy.hp <= 0:
                    enemies.remove(enemy)
                    player.points += 1
                notifications.append(Notification(bullet.x, bullet.y, 10, "gold", font))
                bullets.remove(bullet)
                break

    player.draw(screen)

    if player.hp <= 0:

        screen.fill((0, 0, 0))
        go_text = font.render("GAME OVER", True, (255, 0, 0))
        info_text = font.render("Press ESC or close window", True, (200, 200, 200))
        screen.blit(go_text, (SCREEN_WIDTH//2 - go_text.get_width()//2, SCREEN_HEIGHT//2 - 40))
        screen.blit(info_text, (SCREEN_WIDTH//2 - info_text.get_width()//2, SCREEN_HEIGHT//2 + 10))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    waiting = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    waiting = False
            clock.tick(30)
        running = False

    pygame.display.update()

pygame.quit()