"""
Circular hitbox for collision detection.

This module provides a circular hitbox implementation that uses
circle-circle collision detection algorithm for efficient and
accurate collision checking between game objects.
"""
import pygame
from typing import Tuple


class HitBox:
    """
    Circular hitbox for collision detection between game objects.
    
    The hitbox uses a simple circle representation with a center point (x, y)
    and radius. It provides efficient circle-circle collision detection using
    the distance formula optimization (avoiding expensive sqrt operations).
    
    Attributes:
        x (float): Center X position of the hitbox
        y (float): Center Y position of the hitbox
        r (float): Radius of the circular hitbox
        size_offset (float): Offset applied to center the hitbox on sprites
    """
    
    def __init__(self, x: float, y: float, radius: float, size_offset: float = 0) -> None:
        """
        Initialize a circular hitbox.
        
        Args:
            x: Initial X position (top-left corner of the bounding box)
            y: Initial Y position (top-left corner of the bounding box)
            radius: Radius of the collision circle
            size_offset: Offset to center the hitbox on the sprite
                        (typically half the sprite size)
        
        Raises:
            ValueError: If radius is negative or zero
        """
        if radius <= 0:
            raise ValueError(f"Radius must be positive, got {radius}")
        
        self.x = x + size_offset
        self.y = y + size_offset
        self.r = radius
        self.size_offset = size_offset
    
    @property
    def position(self) -> Tuple[float, float]:
        """
        Get the current position of the hitbox (without offset).
        
        Returns:
            Tuple of (x, y) coordinates representing the top-left position
        """
        return self.x - self.size_offset, self.y - self.size_offset
    
    @property
    def center(self) -> Tuple[float, float]:
        """
        Get the center position of the hitbox.
        
        Returns:
            Tuple of (x, y) coordinates representing the center position
        """
        return self.x, self.y
    
    def update_position(self, x: float, y: float) -> None:
        """
        Update the hitbox position.
        
        This method updates the center position of the hitbox based on
        the provided top-left coordinates, automatically applying the
        size offset to maintain proper centering.
        
        Args:
            x: New X position (top-left corner)
            y: New Y position (top-left corner)
        """
        self.x = x + self.size_offset
        self.y = y + self.size_offset

    def collide(self, other: "HitBox") -> bool:
        """
        Check collision with another hitbox using circle-circle detection.
        
        This method uses an optimized collision detection algorithm that
        compares squared distances to avoid the expensive square root operation.
        Two circles collide when the distance between their centers is less than
        or equal to the sum of their radii.
        
        Mathematical formula:
        distance² = (x₁ - x₂)² + (y₁ - y₂)²
        collision = distance² <= (r₁ + r₂)²
        
        Args:
            other: Another HitBox instance to check collision against
            
        Returns:
            True if the hitboxes are overlapping, False otherwise
        """
        # Calculate squared distance between centers (avoids sqrt for performance)
        distance_sq = (self.x - other.x) ** 2 + (self.y - other.y) ** 2
        
        # Check if squared distance is less than squared sum of radii
        sum_of_radii_sq = (self.r + other.r) ** 2
        
        return distance_sq <= sum_of_radii_sq
    
    def get_position(self) -> Tuple[float, float]:
        """
        Get the current position without offset (deprecated).
        
        Note:
            This method is deprecated. Use the 'position' property instead.
        
        Returns:
            Tuple of (x, y) coordinates
        """
        return self.position
    
    def draw_debug(self, screen: pygame.Surface, color: Tuple[int, int, int] = (255, 0, 0), 
                   width: int = 2) -> None:
        """
        Draw the hitbox outline for debugging purposes.
        
        This method visualizes the hitbox as a circle outline on the screen,
        which is useful for debugging collision detection issues and verifying
        hitbox positioning.
        
        Args:
            screen: Pygame surface to draw on
            color: RGB color tuple for the debug circle (default: red)
            width: Line width in pixels (default: 2)
        """
        pygame.draw.circle(
            screen, 
            color, 
            (int(self.x), int(self.y)), 
            int(self.r), 
            width
        )
    
    def __repr__(self) -> str:
        """
        String representation of the HitBox for debugging.
        
        Returns:
            String representation showing position and radius
        """
        return f"HitBox(x={self.x:.1f}, y={self.y:.1f}, radius={self.r:.1f})"
