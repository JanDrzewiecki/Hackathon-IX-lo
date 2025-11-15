"""
Utilities package for the game.

This package contains utility classes and functions following SOLID principles:
- HitBox: Circular collision detection
- Particles: Visual effects system (particles, blood effects, gravestones)
- Vector2D: 2D vector mathematics
- CollisionDetector: Various collision detection algorithms

Each module has a single, well-defined responsibility and is designed to be
reusable and testable.
"""

# Import commonly used classes for convenient access
from src.utils.hitbox import HitBox
from src.utils.particles import Particle, BloodParticleSystem, Gravestone
from src.utils.vector2d import Vector2D
from src.utils.collision_detector import CollisionDetector

__all__ = [
    'HitBox',
    'Particle',
    'BloodParticleSystem',
    'Gravestone',
    'Vector2D',
    'CollisionDetector',
]
