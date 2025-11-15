"""
Main game entry point - Uranek Reactor Run
Refactored to use modular components from src/ directory
"""
import pygame
import random
from pygame.locals import *

# Import refactored modules
from src.entities.player import Player
from src.managers.enemy_spawner import EnemySpawner
from src.ui.notification import Notification
from src.entities.bullet import Bullet
from src.core.constants import *
from src.managers.room_manager import RoomManager
from src.managers.final_room_manager import FinalRoomManager
from src.ui.hud import HeartsHUD
from src.utils.particles import BloodParticleSystem
from src.ui.map_text import EuroAsiaMapText, NorthSouthAmericaMapText, AfricaMapText, AustraliaMapText
from src.managers.background_manager import RoomBackgroundManager
from src.managers.powerup_manager import PowerUpManager
from src.managers.enemy_bullet_manager import EnemyBulletManager
from src.managers.powerup_pickup_manager import PowerUpPickupManager
from src.ui.screens import show_start_screen, show_about_screen, show_map, show_game_over
from src.ui.boss_bar import BossBarManager

# Initialize Pygame
pygame.init()

# Fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Hackaton Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri.ttf", 30)

# Initialize background manager
bg_manager = RoomBackgroundManager()
room_background, _ = bg_manager.get_random_background()

# Load power-up icons for HUD
shoe_icon = None
shield_icon = None
sword_icon = None

try:
    shoe_icon = pygame.image.load("game/boost_shoe2.png").convert_alpha()
    shoe_icon = pygame.transform.smoothscale(shoe_icon, (40, 40))
except:
    try:
        shoe_icon = pygame.image.load("boost_shoe2.png").convert_alpha()
        shoe_icon = pygame.transform.smoothscale(shoe_icon, (40, 40))
    except:
        print("Warning: Could not load boost_shoe2.png")

try:
    shield_icon = pygame.image.load("game/shield.png").convert_alpha()
    shield_icon = pygame.transform.smoothscale(shield_icon, (40, 40))
except:
    try:
        shield_icon = pygame.image.load("shield.png").convert_alpha()
        shield_icon = pygame.transform.smoothscale(shield_icon, (40, 40))
    except:
        print("Warning: Could not load shield.png")

try:
    sword_icon = pygame.image.load("game/swordbg.png").convert_alpha()
    sword_icon = pygame.transform.smoothscale(sword_icon, (40, 40))
except:
    try:
        sword_icon = pygame.image.load("swordbg.png").convert_alpha()
        sword_icon = pygame.transform.smoothscale(sword_icon, (40, 40))
    except:
        try:
            sword_icon = pygame.image.load("game/sword.png").convert_alpha()
            sword_icon = pygame.transform.smoothscale(sword_icon, (40, 40))
        except:
            try:
                sword_icon = pygame.image.load("sword.png").convert_alpha()
                sword_icon = pygame.transform.smoothscale(sword_icon, (40, 40))
            except:
                print("Warning: Could not load swordbg.png or sword.png")

# Load map images
def load_image(paths):
    """Try to load image from multiple paths"""
    for path in paths:
        try:
            return pygame.image.load(path).convert()
        except:
            continue
    return None

map_image = load_image(["game/map.png", "map.png"])
map2_image = load_image(["game/map2.png", "map2.png"])
map3_image = load_image(["game/map3.png", "map3.png"])
map4_image = load_image(["game/map4.png", "map4.png"])
start_screen_image = load_image(["game/ekran_startowy.png", "ekran_startowy.png"])

if not map_image:
    print("Warning: Could not load map.png")
if not map2_image:
    print("Warning: Could not load map2.png")
if not map3_image:
    print("Warning: Could not load map3.png")
if not map4_image:
    print("Warning: Could not load map4.png")
if not start_screen_image:
    print("Warning: Could not load ekran_startowy.png")


def start_new_game(keep_current_level=False):
    """Reset all game state to start a fresh run."""
    global room_manager, player, enemies, level, enemy_spawner, notifications
    global bullets, bullets_cooldown
    global visited_rooms, cleared_rooms, hud, blood_systems, boss_killed, current_level, room_background
    global powerup_manager, boss_bar_manager, enemy_bullet_manager, powerup_pickup_manager

    # Store current level if we need to keep it
    saved_level = current_level if keep_current_level else 1

    # Store power-up charges if transitioning between levels
    if keep_current_level:
        saved_charges = powerup_manager.get_charges()
        saved_last_powerup = powerup_pickup_manager.last_powerup_type
    else:
        saved_charges = {'speed': 0, 'shield': 0, 'strength': 0}
        saved_last_powerup = None

    # Choose random background for the level
    room_background, _ = bg_manager.get_random_background(level=saved_level)

    # Create room manager
    if saved_level == 4:
        room_manager = FinalRoomManager(SCREEN_WIDTH, SCREEN_HEIGHT, margin_pixels=100)
    else:
        room_manager = RoomManager(SCREEN_WIDTH, SCREEN_HEIGHT, margin_pixels=100)

    # Create player in center
    player_start_x = room_manager.room_x + room_manager.room_width // 2 - URANEK_FRAME_WIDTH // 2
    player_start_y = room_manager.room_y + room_manager.room_height // 2 - URANEK_FRAME_WIDTH // 2
    player = Player(player_start_x, player_start_y)

    # Initialize game state
    enemies = []
    level = saved_level
    enemy_spawner = EnemySpawner(level, room_manager)
    notifications = []
    bullets = []
    bullets_cooldown = 0
    blood_systems = []
    visited_rooms = {0}
    cleared_rooms = set()
    boss_killed = False
    current_level = saved_level
    hud = HeartsHUD()

    # Reset managers and restore state
    powerup_manager.reset(keep_charges=False)
    powerup_manager.set_charges(**saved_charges)
    boss_bar_manager.reset()
    enemy_bullet_manager.clear()
    powerup_pickup_manager.reset_for_new_level()
    powerup_pickup_manager.last_powerup_type = saved_last_powerup
    
    enemy_spawner.reset_for_new_room()


# Initialize global variables
room_manager = None
player = None
enemies = []
level = 1
enemy_spawner = None
notifications = []
bullets = []
bullets_cooldown = 0
blood_systems = []
visited_rooms = {0}
cleared_rooms = set()
boss_killed = False
current_level = 1
hud = None

# Power-up manager
powerup_manager = PowerUpManager()

# Boss bar manager
boss_bar_manager = BossBarManager(SCREEN_WIDTH, SCREEN_HEIGHT)

# Enemy bullet manager
enemy_bullet_manager = EnemyBulletManager(SCREEN_WIDTH, SCREEN_HEIGHT, FPS)

# Power-up pickup manager
powerup_pickup_manager = PowerUpPickupManager()


# Initial game state - Show start screen first
running = True
game_started = False

while running and not game_started:
    action = show_start_screen(screen, start_screen_image, clock, SCREEN_WIDTH, SCREEN_HEIGHT)
    if action == 'start':
        result = show_map(screen, map_image, font, clock, SCREEN_WIDTH, SCREEN_HEIGHT)
        if result == "skip_to_level_3":
            current_level = 3
            start_new_game(keep_current_level=True)
        else:
            start_new_game()
        game_started = True
    elif action == 'about':
        result = show_about_screen(screen, font, clock, SCREEN_WIDTH, SCREEN_HEIGHT)
        if result == 'quit':
            running = False
    elif action == 'quit':
        running = False

# Main game loop
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    # Draw room background
    if room_background and not isinstance(room_manager, FinalRoomManager):
        scaled_bg = pygame.transform.scale(room_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))

    # Check if current room is cleared
    room_cleared = room_manager.current_room_id in cleared_rooms

    # Update door animation
    room_manager.update_door_animation(room_cleared)

    # Draw room with corridors
    room_manager.draw(screen, boss_killed, room_cleared)

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed()

    # Shooting
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        mx, my = pygame.mouse.get_pos()
        if bullets_cooldown <= 0:
            bullets.append(Bullet(player, mx, my, powerup_manager.is_strength_active()))
            bullets_cooldown = FPS / 3

    did_teleport = player.update(keys, room_manager, visited_rooms, enemies, boss_killed)

    # Handle special corridor (NEXT LEVEL after boss)
    if did_teleport == "next_level":
        current_level += 1
        # Show appropriate map
        if current_level == 2 and map2_image:
            result = show_map(screen, map2_image, font, clock, SCREEN_WIDTH, SCREEN_HEIGHT, level_num=2, show_text=True, text_class=NorthSouthAmericaMapText)
            if result == "skip_to_level_3":
                current_level = 3
        elif current_level == 3 and map3_image:
            result = show_map(screen, map3_image, font, clock, SCREEN_WIDTH, SCREEN_HEIGHT, level_num=3, show_text=True, text_class=AfricaMapText)
        elif current_level == 4 and map4_image:
            result = show_map(screen, map4_image, font, clock, SCREEN_WIDTH, SCREEN_HEIGHT, level_num=4, show_text=True, text_class=AustraliaMapText)
        else:
            result = show_map(screen, map_image, font, clock, SCREEN_WIDTH, SCREEN_HEIGHT, level_num=current_level)
            if result == "skip_to_level_3":
                current_level = 3
        start_new_game(keep_current_level=True)
        continue

    # Handle room transition
    if did_teleport:
        room_background, _ = bg_manager.get_random_background(level=current_level)
        visited_rooms.add(room_manager.current_room_id)
        enemies.clear()
        
        if room_manager.current_room_id not in cleared_rooms:
            enemy_spawner.reset_for_new_room()
            powerup_pickup_manager.reset_for_new_room()
        else:
            enemy_spawner.enemies_spawned_in_room = enemy_spawner.max_enemies_for_room
            powerup_pickup_manager.reset_for_new_room()
        
        notifications.append(Notification(player.x, player.y, f"Room {room_manager.current_room_id}", "cyan", font))

    # Spawn enemies only if room is not cleared
    if room_manager.current_room_id not in cleared_rooms:
        prev_enemies_len = len(enemies)
        enemy_spawner.update(enemies)
        
        # Detect newly spawned boss
        if len(enemies) > prev_enemies_len:
            for ne in enemies[prev_enemies_len:]:
                if getattr(ne, 'is_boss', False):
                    boss_bar_manager.activate(ne, notifications, font, player.x, player.y)
                    break

    # Check if room is now cleared
    if (room_manager.current_room_id not in cleared_rooms and 
        enemy_spawner.enemies_spawned_in_room >= enemy_spawner.max_enemies_for_room and 
        len(enemies) == 0):
        
        cleared_rooms.add(room_manager.current_room_id)

        if current_level == 4 and room_manager.current_room_id == 0:
            # Final boss defeated
            notifications.append(Notification(player.x, player.y, "FINAL BOSS DEFEATED!", "gold", font))
            for notification in notifications:
                notification.draw(screen)
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()
            exit()
        elif room_manager.current_room_id == 5:
            boss_killed = True
            notifications.append(Notification(player.x, player.y, "NASTĘPNY POZIOM!", "gold", font))
        else:
            notifications.append(Notification(player.x, player.y, "Room Cleared!", "green", font))

    # Update enemies
    for enemy in enemies:
        enemy.update(player.x, player.y, enemy_bullet_manager.get_bullets())
        enemy.check_collision_with_enemies(enemies)
        enemy.draw(screen)
        
        # Contact damage
        if player.hit_box.collide(enemy.hit_box):
            if powerup_manager.is_shield_active():
                pass  # no damage while shielded
            elif enemy_bullet_manager.get_damage_cooldown() <= 0:
                player.hp = max(0, player.hp - enemy.ad)
                enemy_bullet_manager.damage_cooldown = int(FPS * 0.75)

    # Update notifications
    for notification in notifications:
        notification.update(notifications)
        notification.draw(screen)

    # Draw and check power-up collection
    powerup_pickup_manager.update_and_draw(screen)
    powerup_pickup_manager.check_collection(player, powerup_manager, notifications, font)

    # Update bullets
    for bullet in bullets:
        bullet.update()
        bullet.draw(screen)

    # Check bullet collisions with enemies
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.hit_box.collide(enemy.hit_box):
                enemy.hp -= bullet.ad
                if enemy.hp <= 0:
                    # Create green blood particle explosion
                    blood_systems.append(BloodParticleSystem(enemy.x, enemy.y, num_particles=25))
                    # Handle potential power-up drop
                    powerup_pickup_manager.handle_enemy_death(enemy)
                    enemies.remove(enemy)
                    player.points += 1
                bullets.remove(bullet)
                break

    # Update blood particle systems
    for blood_system in blood_systems[:]:
        blood_system.update()
        blood_system.draw(screen)
        if not blood_system.is_alive():
            blood_systems.remove(blood_system)

    # Update and draw enemy bullets
    enemy_bullet_manager.update_and_draw(screen, player, powerup_manager)

    bullets_cooldown -= 1

    # Handle power-up input and timers
    powerup_manager.handle_input(keys, player, notifications, font)
    powerup_manager.update_timers(player, notifications, font)

    # Remove off-screen bullets
    for bullet in bullets[:]:
        if bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
            bullets.remove(bullet)

    # Draw player
    player.draw(screen)

    # Draw HUD
    hud.draw(screen, player)

    # Update and draw boss HP bar
    boss_bar_manager.update(enemies)
    boss_bar_manager.draw(screen, enemies)

    # Display power-up charges HUD
    powerup_manager.draw_hud(screen, font, SCREEN_HEIGHT, shoe_icon, shield_icon, sword_icon)

    # Display room info
    room_text = font.render(f"Room: {room_manager.current_room_id}", True, (255, 255, 255))
    screen.blit(room_text, (SCREEN_WIDTH - room_text.get_width() - 20, 20))

    visited_text = font.render(f"Visited: {sorted(visited_rooms)}", True, (200, 200, 200))
    screen.blit(visited_text, (SCREEN_WIDTH - visited_text.get_width() - 20, 60))

    level_text = font.render(f"Level: {current_level}", True, (255, 215, 0))
    screen.blit(level_text, (20, 100))

    if cleared_rooms:
        cleared_text = font.render(f"Cleared: {sorted(cleared_rooms)}", True, (100, 255, 100))
        screen.blit(cleared_text, (SCREEN_WIDTH - cleared_text.get_width() - 20, 100))

    # Check for game over
    if player.hp <= 0:
        result = show_game_over(screen, font, clock, SCREEN_WIDTH, SCREEN_HEIGHT)
        if result == 'restart':
            start_new_game()
        else:
            running = False

    pygame.display.update()

pygame.quit()
