"""
Typy wrogów wraz z konfiguracją statystyk.
"""
from enum import Enum
from typing import Dict, Any


class EnemyType(Enum):
    """Typy wrogów o różnym poziomie trudności."""
    WEAK = 1
    MEDIUM = 2
    STRONG = 3
    BOSS = 4
    FINAL_BOSS = 5


class EnemyTypeConfig:
    """Konfiguracja dla każdego typu wroga."""
    
    CONFIGS: Dict[EnemyType, Dict[str, Any]] = {
        EnemyType.WEAK: {
            'hp': 30,
            'ad': 10,
            'speed': 2,
            'count': 6,
            'color': (100, 255, 100),
            'size': 32
        },
        EnemyType.MEDIUM: {
            'hp': 50,
            'ad': 10,
            'speed': 2.5,
            'count': 4,
            'color': (255, 200, 100),
            'size': 40
        },
        EnemyType.STRONG: {
            'hp': 70,
            'ad': 20,
            'speed': 3,
            'count': 2,
            'color': (255, 100, 100),
            'size': 48
        },
        EnemyType.BOSS: {
            'hp': 200,
            'ad': 30,
            'speed': 1.5,
            'count': 1,
            'color': (150, 0, 150),
            'size': 64,
            'shoot_cooldown': 90
        },
        EnemyType.FINAL_BOSS: {
            'hp': 300,
            'ad': 40,
            'speed': 1.2,
            'count': 1,
            'color': (200, 0, 0),
            'size': 64,
            'shoot_cooldown': 20
        }
    }
    
    @classmethod
    def get_config(cls, enemy_type: EnemyType) -> Dict[str, Any]:
        """Zwraca pełną konfigurację dla danego typu wroga."""
        return cls.CONFIGS[enemy_type]
    
    @classmethod
    def get_hp(cls, enemy_type: EnemyType) -> int:
        """Zwraca HP dla danego typu wroga."""
        return cls.CONFIGS[enemy_type]['hp']
    
    @classmethod
    def get_ad(cls, enemy_type: EnemyType) -> int:
        """Zwraca atak dla danego typu wroga."""
        return cls.CONFIGS[enemy_type]['ad']
    
    @classmethod
    def get_speed(cls, enemy_type: EnemyType) -> float:
        """Zwraca prędkość dla danego typu wroga."""
        return cls.CONFIGS[enemy_type]['speed']
    
    @classmethod
    def get_count(cls, enemy_type: EnemyType) -> int:
        """Zwraca liczbę wrogów do zespawnowania."""
        return cls.CONFIGS[enemy_type]['count']
    
    @classmethod
    def get_color(cls, enemy_type: EnemyType) -> tuple:
        """Zwraca kolor dla danego typu wroga."""
        return cls.CONFIGS[enemy_type]['color']
    
    @classmethod
    def get_size(cls, enemy_type: EnemyType) -> int:
        """Zwraca rozmiar dla danego typu wroga."""
        return cls.CONFIGS[enemy_type]['size']
