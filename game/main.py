import pygame
from pygame.locals import *
from settings import *
from player import *
from enemy_spawner import *
from notification import *
from bullet import *
from hud import HeartsHUD

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vampire_Survivor")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri.ttf", 30)

player = Player()
enemies = []
level = 1
enemy_spawner = EnemySpawner(level)
notifications = []
bullets = []
bullets_cooldown = 0
damage_cooldown = 0


hud = HeartsHUD()


running = True

while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

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
    for bullet in bullets:
        if bullet.y > SCREEN_HEIGHT or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.x < 0:
            bullets.remove(bullet)

    player.update()
    player.draw(screen)

    # Draw HP hearts (serduszka)
    hud.draw(screen, player)

    for bullet in bullets:
        for enemy in enemies:
            if bullet.hit_box.collide(enemy.hit_box):
                enemy.hp -= bullet.ad
                if enemy.hp <= 0:
                    enemies.remove(enemy)
                    player.points += 1
                notifications.append(Notification(bullet.x, bullet.y, 10, "gold", font))
                bullets.remove(bullet)

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