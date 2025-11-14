import pygame
from pygame.locals import *
from player import *
from enemy_spawner import *
from notification import *
from bullet import *
from settings import *
from room_manager import RoomManager

pygame.init()

# Fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Vampire_Survivor")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri.ttf", 30)

# Create room manager with corridors
room_manager = RoomManager(SCREEN_WIDTH, SCREEN_HEIGHT, margin_pixels=100)
GAME_AREA_X = room_manager.room_x
GAME_AREA_Y = room_manager.room_y
GAME_AREA_WIDTH = room_manager.room_width
GAME_AREA_HEIGHT = room_manager.room_height

# Create player in center of game area
player_start_x = GAME_AREA_X + GAME_AREA_WIDTH // 2 - PLAYER_SIZE // 2
player_start_y = GAME_AREA_Y + GAME_AREA_HEIGHT // 2 - PLAYER_SIZE // 2
player = Player(player_start_x, player_start_y)
enemies = []
level = 1
enemy_spawner = EnemySpawner(level, room_manager)
notifications = []
bullets = []
bullets_cooldown = 0

# Track visited rooms
visited_rooms = {0}  # Start room is visited

running = True

while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))  #(R,G,B)

    # Draw room with corridors
    room_manager.draw(screen)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    # Store old position for corridor check
    old_x, old_y = player.x, player.y

    # Movement with corridor support
    if keys[pygame.K_a]:
        player.x = player.x - player.movement
    if keys[pygame.K_d]:
        player.x = player.x + player.movement
    if keys[pygame.K_w]:
        player.y = player.y - player.movement
    if keys[pygame.K_s]:
        player.y = player.y + player.movement

    # Clamp position to room or corridor
    player.x, player.y = room_manager.clamp_position(player.x, player.y, PLAYER_SIZE)

    # Check for corridor transition (teleportation to new room)
    should_transition, new_x, new_y, exit_direction = room_manager.check_corridor_transition(
        player.x, player.y, PLAYER_SIZE)

    if should_transition:
        # Teleport player to opposite corridor
        player.x, player.y = new_x, new_y
        # Mark new room as visited
        visited_rooms.add(room_manager.current_room_id)
        # Clear enemies when changing rooms
        enemies.clear()
        # Add notification showing room number
        notifications.append(Notification(player.x, player.y, f"Room {room_manager.current_room_id}", "cyan", font))

    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        x, y = pygame.mouse.get_pos()
        if bullets_cooldown <= 0:
            bullets.append(Bullet(player,  x , y))
            bullets_cooldown = FPS / 3





    enemy_spawner.update(enemies)


    for enemy in enemies:
        enemy.update(player.x, player.y)
        enemy.draw(screen)

    for notification in notifications:
        notification.update(notifications)
        notification.draw(screen)

    for bullet in bullets:
        bullet.update(bullets)
        bullet.draw(screen)

    bullets_cooldown -= 1
    for bullet in bullets[:]:
        if bullet.y > SCREEN_HEIGHT or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.x < 0:
            bullets.remove(bullet)

    player.update()
    player.draw(screen)

    # Display current room and visited rooms
    room_text = font.render(f"Room: {room_manager.current_room_id}", True, (255, 255, 255))
    screen.blit(room_text, (20, 20))

    visited_text = font.render(f"Visited: {sorted(visited_rooms)}", True, (200, 200, 200))
    screen.blit(visited_text, (20, 60))

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







    pygame.display.update()



pygame.quit()
