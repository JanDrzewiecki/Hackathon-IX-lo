#!/usr/bin/env python3
"""Quick test to verify the game starts without errors"""
import sys
import os

# Add game directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'game'))

print("Testing notification color handling...")
from notification import Notification
import pygame

pygame.init()
font = pygame.font.SysFont("Arial", 30)

# Test different color types
test_cases = [
    ("gold", 10),
    ("cyan", "Room 1"),
    ("green", "Room Cleared!"),
    ((255, 0, 0), "Red text"),
]

screen = pygame.display.set_mode((800, 600))

for color, value in test_cases:
    try:
        notif = Notification(100, 100, value, color, font)
        notif.draw(screen)
        print(f"✓ Color {color} with value {value} works!")
    except Exception as e:
        print(f"✗ Color {color} with value {value} FAILED: {e}")
        sys.exit(1)

print("\nTesting enemy drawing...")
from enemy import Enemy
from enemy_type import EnemyType

try:
    weak_enemy = Enemy(100, 100, EnemyType.WEAK)
    medium_enemy = Enemy(200, 100, EnemyType.MEDIUM)
    strong_enemy = Enemy(300, 100, EnemyType.STRONG)
    boss_enemy = Enemy(400, 100, EnemyType.BOSS)

    weak_enemy.draw(screen)
    medium_enemy.draw(screen)
    strong_enemy.draw(screen)
    boss_enemy.draw(screen)

    print("✓ All enemy types draw successfully!")
    print("✓ WEAK and MEDIUM should show sprites without colored rectangles")
    print("✓ STRONG and BOSS should show colored rectangles")
except Exception as e:
    print(f"✗ Enemy drawing FAILED: {e}")
    sys.exit(1)

pygame.quit()
print("\n✓✓✓ All tests passed! ✓✓✓")

