"""Quick test to verify enemy types are working"""
import sys
sys.path.append('game')

from enemy_type import EnemyType, EnemyTypeConfig
from enemy import Enemy

print("\n=== Testing Enemy Types ===\n")

# Test each enemy type
for enemy_type in [EnemyType.WEAK, EnemyType.MEDIUM, EnemyType.STRONG]:
    enemy = Enemy(100, 100, enemy_type)
    config = EnemyTypeConfig.get_config(enemy_type)

    print(f"{enemy_type.name}:")
    print(f"  HP: {enemy.hp} (expected: {config['hp']})")
    print(f"  AD: {enemy.ad} (expected: {config['ad']})")
    print(f"  Speed: {enemy.movement} (expected: {config['speed']})")
    print(f"  Color: {enemy.color} (expected: {config['color']})")
    print(f"  Size: {enemy.size} (expected: {config['size']})")
    print(f"  Count: {config['count']}")

    # Verify
    assert enemy.hp == config['hp'], f"HP mismatch for {enemy_type.name}"
    assert enemy.ad == config['ad'], f"AD mismatch for {enemy_type.name}"
    assert enemy.movement == config['speed'], f"Speed mismatch for {enemy_type.name}"
    assert enemy.color == config['color'], f"Color mismatch for {enemy_type.name}"
    assert enemy.size == config['size'], f"Size mismatch for {enemy_type.name}"

    print("  ✓ All stats correct!\n")

print("=== All tests passed! ===")

