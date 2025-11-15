"""
Collision detection utilities following the Single Responsibility Principle.

This module provides various collision detection algorithms separated into
focused, testable functions. Each function handles one specific type of
collision detection.
"""
import pygame
from typing import Tuple, Optional
from src.utils.hitbox import HitBox
from src.utils.vector2d import Vector2D


class CollisionDetector:
    """
    Static utility class for various collision detection algorithms.
    
    This class provides different collision detection methods following
    the Open/Closed Principle - new collision types can be added without
    modifying existing code.
    
    All methods are static as collision detection is stateless and doesn't
    require instance data.
    """
    
    @staticmethod
    def circle_circle(x1: float, y1: float, r1: float, 
                     x2: float, y2: float, r2: float) -> bool:
        """
        Circle-circle collision detection.
        
        Two circles collide when the distance between their centers is
        less than or equal to the sum of their radii. This implementation
        uses squared distances to avoid expensive sqrt operations.
        
        Mathematical formula:
        distance² = (x₁ - x₂)² + (y₁ - y₂)²
        collision = distance² <= (r₁ + r₂)²
        
        Args:
            x1: X position of first circle's center
            y1: Y position of first circle's center
            r1: Radius of first circle
            x2: X position of second circle's center
            y2: Y position of second circle's center
            r2: Radius of second circle
            
        Returns:
            True if circles are overlapping, False otherwise
            
        Example:
            >>> CollisionDetector.circle_circle(100, 100, 20, 150, 150, 30)
            False
        """
        # Calculate squared distance between centers
        distance_sq = (x1 - x2) ** 2 + (y1 - y2) ** 2
        
        # Calculate squared sum of radii
        sum_of_radii_sq = (r1 + r2) ** 2
        
        return distance_sq <= sum_of_radii_sq
    
    @staticmethod
    def hitbox_hitbox(hitbox1: HitBox, hitbox2: HitBox) -> bool:
        """
        Check collision between two HitBox instances.
        
        Delegates to the HitBox.collide method for consistency.
        
        Args:
            hitbox1: First HitBox instance
            hitbox2: Second HitBox instance
            
        Returns:
            True if hitboxes are colliding, False otherwise
        """
        return hitbox1.collide(hitbox2)
    
    @staticmethod
    def point_circle(px: float, py: float, cx: float, cy: float, r: float) -> bool:
        """
        Point-circle collision detection.
        
        A point is inside a circle if the distance from the point to the
        circle's center is less than or equal to the radius.
        
        Args:
            px: X position of the point
            py: Y position of the point
            cx: X position of the circle's center
            cy: Y position of the circle's center
            r: Radius of the circle
            
        Returns:
            True if point is inside the circle, False otherwise
        """
        distance_sq = (px - cx) ** 2 + (py - cy) ** 2
        return distance_sq <= r ** 2
    
    @staticmethod
    def rect_rect(x1: float, y1: float, w1: float, h1: float,
                  x2: float, y2: float, w2: float, h2: float) -> bool:
        """
        Axis-Aligned Bounding Box (AABB) collision detection.
        
        Two rectangles collide if they overlap on both the X and Y axes.
        This is one of the fastest collision detection methods for
        axis-aligned rectangles.
        
        Args:
            x1, y1: Top-left position of first rectangle
            w1, h1: Width and height of first rectangle
            x2, y2: Top-left position of second rectangle
            w2, h2: Width and height of second rectangle
            
        Returns:
            True if rectangles overlap, False otherwise
        """
        # Check for overlap on X axis
        x_overlap = x1 < x2 + w2 and x1 + w1 > x2
        
        # Check for overlap on Y axis
        y_overlap = y1 < y2 + h2 and y1 + h1 > y2
        
        # Collision occurs if both axes overlap
        return x_overlap and y_overlap
    
    @staticmethod
    def rect_rect_pygame(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
        """
        Pygame Rect collision detection.
        
        A convenience method that uses pygame's built-in collision detection.
        
        Args:
            rect1: First pygame.Rect
            rect2: Second pygame.Rect
            
        Returns:
            True if rectangles collide, False otherwise
        """
        return rect1.colliderect(rect2)
    
    @staticmethod
    def point_rect(px: float, py: float, rx: float, ry: float, 
                   rw: float, rh: float) -> bool:
        """
        Point-rectangle collision detection.
        
        A point is inside a rectangle if it's within the rectangle's bounds
        on both X and Y axes.
        
        Args:
            px: X position of the point
            py: Y position of the point
            rx: X position of the rectangle's top-left corner
            ry: Y position of the rectangle's top-left corner
            rw: Width of the rectangle
            rh: Height of the rectangle
            
        Returns:
            True if point is inside the rectangle, False otherwise
        """
        return (rx <= px <= rx + rw) and (ry <= py <= ry + rh)
    
    @staticmethod
    def circle_rect(cx: float, cy: float, r: float,
                   rx: float, ry: float, rw: float, rh: float) -> bool:
        """
        Circle-rectangle collision detection.
        
        This is a more complex algorithm that checks if a circle overlaps
        with a rectangle. It finds the closest point on the rectangle to
        the circle's center and checks if that point is within the circle.
        
        Args:
            cx: X position of the circle's center
            cy: Y position of the circle's center
            r: Radius of the circle
            rx: X position of the rectangle's top-left corner
            ry: Y position of the rectangle's top-left corner
            rw: Width of the rectangle
            rh: Height of the rectangle
            
        Returns:
            True if circle overlaps with rectangle, False otherwise
        """
        # Find the closest point on the rectangle to the circle's center
        closest_x = max(rx, min(cx, rx + rw))
        closest_y = max(ry, min(cy, ry + rh))
        
        # Check if the closest point is inside the circle
        return CollisionDetector.point_circle(closest_x, closest_y, cx, cy, r)
    
    @staticmethod
    def line_circle(x1: float, y1: float, x2: float, y2: float,
                   cx: float, cy: float, r: float) -> bool:
        """
        Line segment-circle collision detection.
        
        Checks if a line segment intersects with a circle. Uses the
        distance from a point to a line formula.
        
        Args:
            x1, y1: Start point of the line segment
            x2, y2: End point of the line segment
            cx, cy: Center of the circle
            r: Radius of the circle
            
        Returns:
            True if line segment intersects circle, False otherwise
        """
        # First check if either endpoint is inside the circle
        if CollisionDetector.point_circle(x1, y1, cx, cy, r):
            return True
        if CollisionDetector.point_circle(x2, y2, cx, cy, r):
            return True
        
        # Calculate the line segment vector and point-to-start vector
        dx = x2 - x1
        dy = y2 - y1
        fx = x1 - cx
        fy = y1 - cy
        
        # Calculate coefficients for quadratic formula
        a = dx * dx + dy * dy
        b = 2 * (fx * dx + fy * dy)
        c = (fx * fx + fy * fy) - r * r
        
        # Calculate discriminant
        discriminant = b * b - 4 * a * c
        
        # If discriminant is negative, no intersection
        if discriminant < 0:
            return False
        
        # Calculate the parameter t for the intersection points
        discriminant = discriminant ** 0.5
        t1 = (-b - discriminant) / (2 * a)
        t2 = (-b + discriminant) / (2 * a)
        
        # Check if either intersection point is on the line segment (0 <= t <= 1)
        return (0 <= t1 <= 1) or (0 <= t2 <= 1)
    
    @staticmethod
    def get_collision_normal(x1: float, y1: float, x2: float, y2: float) -> Vector2D:
        """
        Calculate the normal vector from object 1 to object 2.
        
        This is useful for calculating reflection or knockback directions
        after a collision.
        
        Args:
            x1, y1: Position of first object
            x2, y2: Position of second object
            
        Returns:
            Normalized Vector2D pointing from object 1 to object 2
        """
        v = Vector2D(x2 - x1, y2 - y1)
        return v.normalize()
    
    @staticmethod
    def get_penetration_depth(x1: float, y1: float, r1: float,
                             x2: float, y2: float, r2: float) -> float:
        """
        Calculate penetration depth for circle-circle collision.
        
        The penetration depth is how much two circles are overlapping.
        This is useful for physics simulations and collision resolution.
        
        Args:
            x1, y1: Center of first circle
            r1: Radius of first circle
            x2, y2: Center of second circle
            r2: Radius of second circle
            
        Returns:
            Penetration depth in pixels (0 if no collision)
        """
        import math
        
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        sum_of_radii = r1 + r2
        
        if distance >= sum_of_radii:
            return 0.0  # No collision
        
        return sum_of_radii - distance
