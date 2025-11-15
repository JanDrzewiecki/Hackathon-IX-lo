#!/usr/bin/env python3
"""
Simple test script to check if level 4 initialization works
"""
import pygame
from settings import *
from final_room_manager import FinalRoomManager
from enemy_spawner import EnemySpawner

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

print("Testing FinalRoomManager initialization...")
try:
    room_manager = FinalRoomManager(SCREEN_WIDTH, SCREEN_HEIGHT, margin_pixels=100)
    print("✓ FinalRoomManager created successfully")
    print(f"  Rooms: {len(room_manager.rooms)}")
    print(f"  Current room ID: {room_manager.current_room_id}")
    print(f"  Room 0 enemy type: {room_manager.rooms[0].enemy_type}")

    print("\nTesting EnemySpawner with FinalRoomManager...")
    enemy_spawner = EnemySpawner(4, room_manager)
    print("✓ EnemySpawner created successfully")

    print("\nTesting reset_for_new_room...")
    enemy_spawner.reset_for_new_room()
    print(f"✓ reset_for_new_room() completed")
    print(f"  Max enemies for room: {enemy_spawner.max_enemies_for_room}")
    print(f"  Enemies spawned: {enemy_spawner.enemies_spawned_in_room}")

    print("\n✅ All tests passed!")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

pygame.quit()

