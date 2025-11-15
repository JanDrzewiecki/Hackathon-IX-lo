"""
Enemy types with different stats
"""
from enum import Enum

class EnemyType(Enum):
    """Four types of enemies with different difficulty"""
    WEAK = 1      # Weakest - 6 enemies, dies in 3 hits
    MEDIUM = 2    # Medium - 4 enemies, dies in 5 hits
    STRONG = 3    # Strong - 2 enemies, dies in 8 hits
    BOSS = 4      # Boss - 1 enemy, dies in 20 hits, shoots projectiles


class EnemyTypeConfig:
    """Configuration for each enemy type"""

    CONFIGS = {
        EnemyType.WEAK: {
            'hp': 30,           # 3 hits * 10 damage = 30 HP
            'ad': 10,           # Attack damage
            'speed': 2,         # Movement speed
            'count': 6,         # Number of enemies to spawn
            'color': (100, 255, 100),  # Light green
            'size': 32
        },
        EnemyType.MEDIUM: {
            'hp': 50,           # 5 hits * 10 damage = 50 HP
            'ad': 10,           # Attack damage
            'speed': 2.5,       # Movement speed
            'count': 4,         # Number of enemies to spawn
            'color': (255, 200, 100),  # Orange
            'size': 40
        },
        EnemyType.STRONG: {
            'hp': 70,           # 7 hits * 10 damage = 70 HP (7 hearts)
            'ad': 20,           # Attack damage
            'speed': 3,         # Movement speed
            'count': 2,         # Number of enemies to spawn
            'color': (255, 100, 100),  # Red
            'size': 100,         # Match sprite size
            'size': 48
        },
        EnemyType.BOSS: {
            'hp': 200,          # 20 hits * 10 damage = 200 HP
            'ad': 30,           # Attack damage
            'speed': 1.5,       # Slower than normal enemies
            'count': 1,         # Only 1 boss
            'color': (150, 0, 150),  # Purple
            'size': 64,         # Larger size
            'shoot_cooldown': 120  # Shoots every 2 seconds (60 FPS * 2)
        }
    }

    @staticmethod
    def get_config(enemy_type: EnemyType):
        """Get configuration for a specific enemy type"""
        return EnemyTypeConfig.CONFIGS[enemy_type]

    @staticmethod
    def get_hp(enemy_type: EnemyType):
        """Get HP for enemy type"""
        return EnemyTypeConfig.CONFIGS[enemy_type]['hp']

    @staticmethod
    def get_ad(enemy_type: EnemyType):
        """Get attack damage for enemy type"""
        return EnemyTypeConfig.CONFIGS[enemy_type]['ad']

    @staticmethod
    def get_speed(enemy_type: EnemyType):
        """Get movement speed for enemy type"""
        return EnemyTypeConfig.CONFIGS[enemy_type]['speed']

    @staticmethod
    def get_count(enemy_type: EnemyType):
        """Get spawn count for enemy type"""
        return EnemyTypeConfig.CONFIGS[enemy_type]['count']

    @staticmethod
    def get_color(enemy_type: EnemyType):
        """Get color for enemy type"""
        return EnemyTypeConfig.CONFIGS[enemy_type]['color']

    @staticmethod
    def get_size(enemy_type: EnemyType):
        """Get size for enemy type"""
        return EnemyTypeConfig.CONFIGS[enemy_type]['size']

