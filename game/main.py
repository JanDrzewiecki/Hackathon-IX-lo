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
pygame.display.set_caption("Hackaton Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri.ttf", 30)

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

running = True

while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

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

    if did_teleport:
        enemies.clear()
        notifications.append(
            Notification(player.x, player.y, "New Room!", "cyan", font)
        )

    # enemy_spawner.update(enemies)

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
        if bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
            bullets.remove(bullet)

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

    pygame.display.update()

pygame.quit()