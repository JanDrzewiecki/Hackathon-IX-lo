#!/usr/bin/env python3
"""Test to verify STRONG enemy has animation"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'game'))

import pygame
from enemy import Enemy
from enemy_type import EnemyType

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create STRONG enemy
strong_enemy = Enemy(400, 300, EnemyType.STRONG)

print(f"STRONG enemy has {len(strong_enemy.frames)} frames loaded")
print(f"Current sprite: {strong_enemy.current_sprite}")

if len(strong_enemy.frames) == 0:
    print("❌ ERROR: STRONG enemy has NO frames!")
    sys.exit(1)

# Track frame changes
frames_seen = set()
player_x, player_y = 200, 300

print("\nRunning animation test for 3 seconds (180 frames)...")
for frame in range(180):
    screen.fill((50, 50, 50))

    # Update enemy (will update animation)
    strong_enemy.update(player_x, player_y)

    # Track which frames we've seen
    frames_seen.add(strong_enemy.frame_index)

    # Draw enemy
    strong_enemy.draw(screen)

    # Draw label
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(f"STRONG enemy - frame {strong_enemy.frame_index}/{len(strong_enemy.frames)-1}", True, (255, 255, 255))
    screen.blit(text, (strong_enemy.x, strong_enemy.y - 30))

    pygame.display.flip()
    clock.tick(60)

    # Check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

pygame.quit()

print(f"\n✓ STRONG enemy has {len(strong_enemy.frames)} total frames")
print(f"✓ Showed {len(frames_seen)} different frames during test: {sorted(frames_seen)}")

if len(frames_seen) > 1:
    print("\n✅✅✅ STRONG enemy animation is WORKING! ✅✅✅")
else:
    print("\n❌ STRONG enemy animation is NOT working (stuck on one frame)")
    sys.exit(1)

