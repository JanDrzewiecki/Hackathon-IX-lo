"""
2D Vector mathematics utilities.

This module provides a Vector2D class for handling 2D position and velocity
calculations in the game. It encapsulates common vector operations following
the Single Responsibility Principle.
"""
import math
from typing import Tuple, Union


class Vector2D:
    """
    A 2D vector for position, velocity, and direction calculations.
    
    This class provides a clean interface for 2D vector mathematics,
    including addition, subtraction, scalar multiplication, normalization,
    and distance calculations.
    
    Attributes:
        x (float): X component of the vector
        y (float): Y component of the vector
    
    Example:
        >>> pos = Vector2D(100, 200)
        >>> vel = Vector2D(5, -3)
        >>> new_pos = pos + vel
        >>> distance = pos.distance_to(Vector2D(150, 250))
    """
    
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        """
        Initialize a 2D vector.
        
        Args:
            x: X component (default: 0.0)
            y: Y component (default: 0.0)
        """
        self.x = float(x)
        self.y = float(y)
    
    @property
    def magnitude(self) -> float:
        """
        Calculate the magnitude (length) of the vector.
        
        Uses the Pythagorean theorem: √(x² + y²)
        
        Returns:
            The length of the vector
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    @property
    def magnitude_squared(self) -> float:
        """
        Calculate the squared magnitude of the vector.
        
        This is faster than magnitude() as it avoids the sqrt operation.
        Useful for distance comparisons where actual distance isn't needed.
        
        Returns:
            The squared length of the vector
        """
        return self.x ** 2 + self.y ** 2
    
    def normalize(self) -> 'Vector2D':
        """
        Return a normalized (unit length) version of this vector.
        
        A normalized vector has the same direction but magnitude of 1.
        This is useful for direction vectors.
        
        Returns:
            A new Vector2D with magnitude 1, or (0, 0) if magnitude is 0
        """
        mag = self.magnitude
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)
    
    def distance_to(self, other: 'Vector2D') -> float:
        """
        Calculate the Euclidean distance to another vector.
        
        Args:
            other: Another Vector2D instance
            
        Returns:
            The distance between this vector and the other
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx ** 2 + dy ** 2)
    
    def distance_squared_to(self, other: 'Vector2D') -> float:
        """
        Calculate the squared distance to another vector.
        
        This is faster than distance_to() and useful for comparisons.
        
        Args:
            other: Another Vector2D instance
            
        Returns:
            The squared distance between vectors
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return dx ** 2 + dy ** 2
    
    def dot(self, other: 'Vector2D') -> float:
        """
        Calculate the dot product with another vector.
        
        The dot product can be used to find the angle between vectors
        or to project one vector onto another.
        
        Args:
            other: Another Vector2D instance
            
        Returns:
            The dot product: x₁*x₂ + y₁*y₂
        """
        return self.x * other.x + self.y * other.y
    
    def angle_to(self, other: 'Vector2D') -> float:
        """
        Calculate the angle to another vector in radians.
        
        Args:
            other: Another Vector2D instance
            
        Returns:
            Angle in radians between this vector and the other
        """
        return math.atan2(other.y - self.y, other.x - self.x)
    
    def rotate(self, angle: float) -> 'Vector2D':
        """
        Return a rotated version of this vector.
        
        Uses rotation matrix:
        x' = x*cos(θ) - y*sin(θ)
        y' = x*sin(θ) + y*cos(θ)
        
        Args:
            angle: Rotation angle in radians
            
        Returns:
            A new rotated Vector2D
        """
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2D(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
    
    def copy(self) -> 'Vector2D':
        """
        Create a copy of this vector.
        
        Returns:
            A new Vector2D with the same components
        """
        return Vector2D(self.x, self.y)
    
    def to_tuple(self) -> Tuple[float, float]:
        """
        Convert to a tuple.
        
        Returns:
            Tuple of (x, y)
        """
        return (self.x, self.y)
    
    def to_int_tuple(self) -> Tuple[int, int]:
        """
        Convert to an integer tuple (useful for pygame).
        
        Returns:
            Tuple of (int(x), int(y))
        """
        return (int(self.x), int(self.y))
    
    # Operator overloading for intuitive vector math
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        """Vector addition: v1 + v2"""
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        """Vector subtraction: v1 - v2"""
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: Union[int, float]) -> 'Vector2D':
        """Scalar multiplication: v * scalar"""
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: Union[int, float]) -> 'Vector2D':
        """Reverse scalar multiplication: scalar * v"""
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar: Union[int, float]) -> 'Vector2D':
        """Scalar division: v / scalar"""
        if scalar == 0:
            raise ValueError("Cannot divide vector by zero")
        return Vector2D(self.x / scalar, self.y / scalar)
    
    def __neg__(self) -> 'Vector2D':
        """Negation: -v"""
        return Vector2D(-self.x, -self.y)
    
    def __eq__(self, other: object) -> bool:
        """Equality comparison: v1 == v2"""
        if not isinstance(other, Vector2D):
            return False
        return self.x == other.x and self.y == other.y
    
    def __repr__(self) -> str:
        """String representation for debugging"""
        return f"Vector2D({self.x:.2f}, {self.y:.2f})"
    
    def __str__(self) -> str:
        """String representation for display"""
        return f"({self.x:.2f}, {self.y:.2f})"
    
    @staticmethod
    def from_angle(angle: float, magnitude: float = 1.0) -> 'Vector2D':
        """
        Create a vector from an angle and magnitude.
        
        Args:
            angle: Angle in radians
            magnitude: Length of the vector (default: 1.0)
            
        Returns:
            A new Vector2D pointing in the given direction
            
        Example:
            >>> right = Vector2D.from_angle(0, 10)  # 10 units to the right
            >>> up = Vector2D.from_angle(math.pi/2, 5)  # 5 units up
        """
        return Vector2D(
            math.cos(angle) * magnitude,
            math.sin(angle) * magnitude
        )
    
    @staticmethod
    def zero() -> 'Vector2D':
        """
        Create a zero vector (0, 0).
        
        Returns:
            A new Vector2D with both components set to 0
        """
        return Vector2D(0, 0)
    
    @staticmethod
    def one() -> 'Vector2D':
        """
        Create a unit vector (1, 1).
        
        Returns:
            A new Vector2D with both components set to 1
        """
        return Vector2D(1, 1)
    
    @staticmethod
    def up() -> 'Vector2D':
        """Create an up-pointing unit vector (0, -1) in screen coordinates"""
        return Vector2D(0, -1)
    
    @staticmethod
    def down() -> 'Vector2D':
        """Create a down-pointing unit vector (0, 1) in screen coordinates"""
        return Vector2D(0, 1)
    
    @staticmethod
    def left() -> 'Vector2D':
        """Create a left-pointing unit vector (-1, 0)"""
        return Vector2D(-1, 0)
    
    @staticmethod
    def right() -> 'Vector2D':
        """Create a right-pointing unit vector (1, 0)"""
        return Vector2D(1, 0)
