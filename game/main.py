import pygame
from pygame.locals import *
from player import *
from enemy_spawner import *
from notification import *
from bullet import *
from settings import *
from room import *

pygame.init()

# Fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Vampire_Survivor")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri.ttf", 30)

# Create room with 200px margin
room = Room(SCREEN_WIDTH, SCREEN_HEIGHT, margin_pixels=100)
GAME_AREA_X = room.x
GAME_AREA_Y = room.y
GAME_AREA_WIDTH = room.width
GAME_AREA_HEIGHT = room.height

# Create player in center of game area
player_start_x = GAME_AREA_X + GAME_AREA_WIDTH // 2 - PLAYER_SIZE // 2
player_start_y = GAME_AREA_Y + GAME_AREA_HEIGHT // 2 - PLAYER_SIZE // 2
player = Player(player_start_x, player_start_y)
enemies = []
level = 1
enemy_spawner = EnemySpawner(level, room)
notifications = []
bullets = []
bullets_cooldown = 0


running = True

while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))  #(R,G,B)

    # Draw room
    room.draw(screen)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False



    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.x > GAME_AREA_X:
        player.x = max(GAME_AREA_X, player.x - player.movement)
    if keys[pygame.K_d] and player.x + PLAYER_SIZE < GAME_AREA_X + GAME_AREA_WIDTH:
        player.x = min(GAME_AREA_X + GAME_AREA_WIDTH - PLAYER_SIZE, player.x + player.movement)
    if keys[pygame.K_w] and player.y > GAME_AREA_Y:
        player.y = max(GAME_AREA_Y, player.y - player.movement)
    if keys[pygame.K_s] and player.y + PLAYER_SIZE < GAME_AREA_Y + GAME_AREA_HEIGHT:
        player.y = min(GAME_AREA_Y + GAME_AREA_HEIGHT - PLAYER_SIZE, player.y + player.movement)

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
