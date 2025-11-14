import pygame
from pygame.locals import *
from player import *
from enemy_spawner import *
from notification import *
from settings import *
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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vampire_Survivor")
screen_width = 800
screen_height = 800
fps = 60
enemies = []
level = 1
enemy_spawner = EnemySpawner(level, room_manager)
notifications = []
bullets = []
bullets_cooldown = 0
damage_cooldown = 0


hud = HeartsHUD()

pozdro = "elo"
running = True

while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    # Draw room with corridors
    room_manager.draw(screen)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    keys = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        x, y = pygame.mouse.get_pos()
        if bullets_cooldown <= 0:
            bullets.append(Bullet(player,  x , y))
            bullets_cooldown = FPS / 3
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

    # Check for corridor transition (teleportation to new room)
    should_transition, new_x, new_y, exit_direction = room_manager.check_corridor_transition(
        player.x, player.y, PLAYER_SIZE)

    if should_transition:
        # Teleport player to opposite corridor
        player.x, player.y = new_x, new_y
        # Clear enemies when changing rooms
        enemies.clear()
        # Optional: Add notification
        notifications.append(Notification(player.x, player.y, "New Room!", "cyan", font))

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
        if bullet.y > SCREEN_HEIGHT or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.x < 0:
            bullets.remove(bullet)

    player.update(pygame.key.get_pressed())
    player.draw(screen)

    hud.draw(screen, player)

    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.hit_box.collide(enemy.hit_box):
                # Enemy loses exactly one heart per hit (no halves)
                dead = enemy.take_hit()
                if dead:
                    enemies.remove(enemy)
                    player.points += 1
                notifications.append(Notification(bullet.x, bullet.y, 10, "gold", font))
                bullets.remove(bullet)
                break

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