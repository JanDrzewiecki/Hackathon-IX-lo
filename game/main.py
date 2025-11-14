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

    player.update(pygame.key.get_pressed())
    player.draw(screen)

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