#!/usr/bin/env python
"""Quick test to verify player movement works"""
from player import Player
from room_manager import RoomManager
from settings import URANEK_FRAME_WIDTH
import pygame

# Initialize pygame
pygame.init()

# Create a test room manager
room_manager = RoomManager(1200, 800, margin_pixels=100)

# Create player in center
player_start_x = room_manager.room_x + room_manager.room_width // 2 - URANEK_FRAME_WIDTH // 2
player_start_y = room_manager.room_y + room_manager.room_height // 2 - URANEK_FRAME_WIDTH // 2
player = Player(player_start_x, player_start_y)

print(f"Initial player position: ({player.x}, {player.y})")
print(f"Player movement speed: {player.movement}")
print(f"Player hitbox: x={player.hit_box.x}, y={player.hit_box.y}, r={player.hit_box.r}")

# Simulate pressing W key (move up)
keys = {pygame.K_w: True, pygame.K_s: False, pygame.K_a: False, pygame.K_d: False}
class KeyDict:
    def __getitem__(self, key):
        return keys.get(key, False)

test_keys = KeyDict()

old_y = player.y
player.update(test_keys, room_manager)
new_y = player.y

print(f"After moving up: ({player.x}, {player.y})")
print(f"Y changed by: {new_y - old_y}")

if old_y != new_y:
    print("✓ Movement is WORKING!")
else:
    print("✗ Movement is NOT working")
    print(f"Room bounds: x={room_manager.room_x}, y={room_manager.room_y}, w={room_manager.room_width}, h={room_manager.room_height}")
    print(f"Number of walls: {len(room_manager.walls)}")
    for i, wall in enumerate(room_manager.walls):
        print(f"  Wall {i}: x={wall.x}, y={wall.y}, w={wall.width}, h={wall.height}")

pygame.quit()

