import pygame
from pygame.locals import *
from player import*
from enemy_spawner import*
from notification import*
from bullet import *

pygame.init()

screen_width = 800
screen_height = 800
fps = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
pygame.display.set_caption("Vampire_Survivor")
clock = pygame.time.Clock()
movement = 10
font = pygame.font.SysFont("Calibri.ttf", 30)

player = Player()
enemies = []
level = 1
enemy_spawner = EnemySpawner(level)
notifications = []
bullets = []
bullets_cooldown = 0


running = True

while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))  #(R,G,B)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False



    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.x - PLAYER_SIZE >= 0:
                player.x -= player.movement
    if keys[pygame.K_d] and player.x < SCREEN_WIDTH:
                player.x += player.movement
    if keys[pygame.K_w] and player.y - PLAYER_SIZE >= 0:
                player.y -= player.movement
    if keys[pygame.K_s] and player.y < SCREEN_HEIGHT:
                player.y += player.movement

    keys = pygame.mouse.get_pos()
    if keys[0]:
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
    for bullet in bullets:
        if bullet.y > SCREEN_HEIGHT or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.x < 0:
            bullets.remove(bullet)

    player.update()
    player.draw(screen)

    for bullet in bullets:
        for enemy in enemies:
            if bullet.hit_box.collide(enemy.hit_box):
                enemy.hp -= bullet.ad
                if enemy.hp <= 0:
                    enemies.remove(enemy)
                    player.points += 1
                notifications.append(Notification(bullet.x, bullet.y, 10, "gold", font))
                bullets.remove(bullet)






    
    pygame.display.update()



pygame.quit()