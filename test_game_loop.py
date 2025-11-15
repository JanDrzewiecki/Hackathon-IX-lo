#!/usr/bin/env python3
"""Test the game starts and runs without crashing"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'game'))

import pygame
from player import Player
from enemy_spawner import EnemySpawner
from notification import Notification
from room_manager import RoomManager
from settings import *

print("Initializing pygame...")
pygame.init()
screen = pygame.display.set_mode((1440, 900))
font = pygame.font.SysFont("Calibri.ttf", 30)

print("Creating game objects...")
room_manager = RoomManager(1440, 900, margin_pixels=100)
player = Player(620, 350)
enemy_spawner = EnemySpawner(1, room_manager)
enemies = []
notifications = []
bullets = []

print("Testing notification creation...")
notifications.append(Notification(player.x, player.y, f"Room {room_manager.current_room_id}", "cyan", font))
notifications.append(Notification(player.x + 50, player.y, "Test Gold", "gold", font))
notifications.append(Notification(player.x + 100, player.y, 10, "gold", font))

print("Spawning enemies...")
for i in range(5):
    enemy_spawner.update(enemies)

print(f"Spawned {len(enemies)} enemies")

print("Running game loop for 10 frames...")
for frame in range(10):
    screen.fill((0, 0, 0))

    # Draw room
    room_manager.draw(screen, False)

    # Update and draw enemies
    for enemy in enemies:
        try:
            enemy.update(player.x, player.y, [])
            enemy.draw(screen)
        except Exception as e:
            print(f"✗ Error updating/drawing enemy: {e}")
            sys.exit(1)

    # Update and draw notifications
    for notification in notifications[:]:
        try:
            notification.update(notifications)
            notification.draw(screen)
        except Exception as e:
            print(f"✗ Error with notification: {e}")
            sys.exit(1)

    # Draw player
    player.draw(screen)

    pygame.display.flip()
    print(f"  Frame {frame + 1}/10 - OK")

pygame.quit()
print("\n✓✓✓ Game runs successfully without crashes! ✓✓✓")
print("\nFixes applied:")
print("1. Removed duplicate colored rectangle drawing over enemy sprites")
print("2. Fixed notification color handling to properly convert string colors to RGB")

