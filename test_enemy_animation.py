#!/usr/bin/env python3
"""Test enemy animation to verify frames are changing"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'game'))

import pygame
from enemy import Enemy
from enemy_type import EnemyType

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create test enemies
weak_enemy = Enemy(200, 300, EnemyType.WEAK)
medium_enemy = Enemy(500, 300, EnemyType.MEDIUM)

print(f"WEAK enemy has {len(weak_enemy.frames)} frames")
print(f"MEDIUM enemy has {len(medium_enemy.frames)} frames")

if len(weak_enemy.frames) == 0:
    print("WARNING: WEAK enemy has no frames loaded!")
if len(medium_enemy.frames) == 0:
    print("WARNING: MEDIUM enemy has no frames loaded!")

# Player position (static for test)
player_x, player_y = 400, 300

# Track frame changes
weak_frames_seen = set()
medium_frames_seen = set()

print("\nRunning animation test for 3 seconds (180 frames)...")
for frame in range(180):
    screen.fill((50, 50, 50))

    # Update enemies (they will chase the player position)
    weak_enemy.update(player_x, player_y)
    medium_enemy.update(player_x, player_y)

    # Track which frames we've seen
    weak_frames_seen.add(weak_enemy.frame_index)
    medium_frames_seen.add(medium_enemy.frame_index)

    # Draw enemies
    weak_enemy.draw(screen)
    medium_enemy.draw(screen)

    # Draw labels
    font = pygame.font.SysFont("Arial", 20)
    weak_text = font.render(f"WEAK (frame {weak_enemy.frame_index})", True, (255, 255, 255))
    medium_text = font.render(f"MEDIUM (frame {medium_enemy.frame_index})", True, (255, 255, 255))
    screen.blit(weak_text, (weak_enemy.x, weak_enemy.y - 30))
    screen.blit(medium_text, (medium_enemy.x, medium_enemy.y - 30))

    pygame.display.flip()
    clock.tick(60)

    # Check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

pygame.quit()

print(f"\n✓ WEAK enemy showed {len(weak_frames_seen)} different frames: {sorted(weak_frames_seen)}")
print(f"✓ MEDIUM enemy showed {len(medium_frames_seen)} different frames: {sorted(medium_frames_seen)}")

if len(weak_frames_seen) > 1:
    print("\n✓✓✓ WEAK enemy animation is WORKING! ✓✓✓")
else:
    print("\n✗✗✗ WEAK enemy animation is NOT working (stuck on one frame)")

if len(medium_frames_seen) > 1:
    print("✓✓✓ MEDIUM enemy animation is WORKING! ✓✓✓")
else:
    print("✗✗✗ MEDIUM enemy animation is NOT working (stuck on one frame)")

