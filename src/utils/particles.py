"""
Particle system for visual effects.

This module provides a flexible particle system for creating visual effects
such as blood splatters, explosions, and other particle-based animations.
It follows the Single Responsibility Principle by separating particle logic,
rendering, and system management into distinct classes.
"""
import pygame
import random
import math
from typing import List, Tuple
from abc import ABC, abstractmethod


class IParticle(ABC):
    """
    Interface for particle objects.
    
    This interface defines the contract that all particle implementations
    must follow, adhering to the Interface Segregation Principle.
    """
    
    @abstractmethod
    def update(self) -> bool:
        """Update particle state. Returns True if particle is still alive."""
        pass
    
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Render the particle on the screen."""
        pass


class Particle(IParticle):
    """
    A single particle with physics and lifetime.
    
    This class represents an individual particle with position, velocity,
    color, and lifetime properties. It simulates simple physics including
    gravity and applies a fade-out effect based on remaining lifetime.
    
    Attributes:
        x (float): Current X position
        y (float): Current Y position
        color (Tuple[int, int, int]): RGB color of the particle
        vx (float): Velocity in X direction
        vy (float): Velocity in Y direction
        lifetime (int): Remaining frames before particle disappears
        max_lifetime (int): Initial lifetime for fade calculation
        size (int): Radius of the particle in pixels
    """
    
    # Physics constants
    GRAVITY = 0.2  # Downward acceleration per frame
    
    def __init__(self, x: float, y: float, color: Tuple[int, int, int], 
                 velocity: Tuple[float, float], lifetime: int) -> None:
        """
        Initialize a particle.
        
        Args:
            x: Initial X position
            y: Initial Y position
            color: RGB color tuple
            velocity: Tuple of (vx, vy) velocity components
            lifetime: How many frames the particle will live
        """
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 5)
    
    def update(self) -> bool:
        """
        Update particle physics and lifetime.
        
        Applies velocity to position and simulates gravity by increasing
        downward velocity. Decrements lifetime counter.
        
        Returns:
            True if particle is still alive (lifetime > 0), False otherwise
        """
        # Apply velocity to position
        self.x += self.vx
        self.y += self.vy
        
        # Apply gravity (increases downward velocity)
        self.vy += self.GRAVITY
        
        # Decrease lifetime
        self.lifetime -= 1
        
        return self.lifetime > 0
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Render the particle with fade-out effect.
        
        The particle's alpha (transparency) is calculated based on the ratio
        of remaining lifetime to initial lifetime, creating a smooth fade-out
        effect as the particle ages.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Calculate alpha based on remaining lifetime (fade out effect)
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color_with_alpha = (*self.color[:3], alpha)
        
        # Create a temporary surface with alpha channel for transparency
        particle_surface = pygame.Surface(
            (self.size * 2, self.size * 2), 
            pygame.SRCALPHA
        )
        pygame.draw.circle(
            particle_surface, 
            color_with_alpha, 
            (self.size, self.size), 
            self.size
        )
        
        # Blit to screen at particle position
        screen.blit(
            particle_surface, 
            (int(self.x - self.size), int(self.y - self.size))
        )


class BloodParticleSystem:
    """
    Particle system for blood splatter effects.
    
    This class manages a collection of particles that simulate a blood
    explosion effect (green blood for enemies). It creates particles in
    a radial explosion pattern and manages their lifecycle.
    
    The system follows the Single Responsibility Principle by focusing
    solely on managing particle lifecycle and rendering.
    
    Attributes:
        particles (List[Particle]): Active particles in the system
        color (Tuple[int, int, int]): Color of the blood particles
    """
    
    # Default configuration constants
    DEFAULT_NUM_PARTICLES = 25
    DEFAULT_COLOR = (0, 255, 0)  # Green blood for enemies
    MIN_PARTICLE_SPEED = 2
    MAX_PARTICLE_SPEED = 8
    MIN_LIFETIME = 30  # frames
    MAX_LIFETIME = 60  # frames
    
    def __init__(self, x: float, y: float, num_particles: int = DEFAULT_NUM_PARTICLES, 
                 color: Tuple[int, int, int] = DEFAULT_COLOR) -> None:
        """
        Initialize a blood particle explosion at the given position.
        
        Creates particles in a radial explosion pattern with random speeds
        and angles for a natural-looking splatter effect.
        
        Args:
            x: X position of the explosion center
            y: Y position of the explosion center
            num_particles: Number of particles to create (default: 25)
            color: RGB color tuple for particles (default: green)
        """
        self.particles: List[Particle] = []
        self.color = color
        
        # Create particles in an explosion pattern
        self._create_explosion(x, y, num_particles)
    
    def _create_explosion(self, x: float, y: float, num_particles: int) -> None:
        """
        Create particles in a radial explosion pattern.
        
        This private method generates particles with random angles and speeds
        to simulate an explosion effect. Uses polar coordinates to distribute
        particles evenly in all directions.
        
        Args:
            x: Center X position
            y: Center Y position
            num_particles: Number of particles to create
        """
        for _ in range(num_particles):
            # Random angle for radial distribution (0 to 2π)
            angle = random.uniform(0, 2 * math.pi)
            
            # Random speed for varied explosion intensity
            speed = random.uniform(self.MIN_PARTICLE_SPEED, self.MAX_PARTICLE_SPEED)
            
            # Convert polar coordinates to Cartesian velocity
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # Random lifetime for varied particle duration
            lifetime = random.randint(self.MIN_LIFETIME, self.MAX_LIFETIME)
            
            # Create and add particle to the system
            particle = Particle(x, y, self.color, (vx, vy), lifetime)
            self.particles.append(particle)
    
    def update(self) -> None:
        """
        Update all particles and remove dead ones.
        
        This method updates each particle's physics and filters out particles
        that have expired (lifetime <= 0), maintaining optimal performance
        by not updating dead particles.
        """
        # Update all particles and keep only alive ones (list comprehension)
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Render all active particles.
        
        Args:
            screen: Pygame surface to draw particles on
        """
        for particle in self.particles:
            particle.draw(screen)
    
    def is_alive(self) -> bool:
        """
        Check if the system has any active particles.
        
        Returns:
            True if there are still particles to render, False otherwise
        """
        return len(self.particles) > 0
    
    def __len__(self) -> int:
        """
        Get the number of active particles.
        
        Returns:
            Number of particles currently in the system
        """
        return len(self.particles)


class Gravestone:
    """
    Gravestone object left behind when an enemy is killed.
    
    This class represents a persistent game object that marks where an
    enemy was defeated. It has collision detection and can be rendered
    with a sprite or fallback graphics.
    
    Attributes:
        x (float): X position of the gravestone
        y (float): Y position of the gravestone
        size (int): Size of the gravestone in pixels
        hit_box (HitBox): Collision detection hitbox
        sprite (pygame.Surface): Loaded gravestone image
    """
    
    DEFAULT_SIZE = 32
    FALLBACK_COLOR_DARK = (100, 100, 100)
    FALLBACK_COLOR_LIGHT = (150, 150, 150)
    FALLBACK_BORDER_WIDTH = 2
    
    def __init__(self, x: float, y: float, size: int = DEFAULT_SIZE) -> None:
        """
        Initialize a gravestone at the given position.
        
        Args:
            x: X position of the gravestone
            y: Y position of the gravestone
            size: Size of the gravestone sprite in pixels (default: 32)
        """
        from src.utils.hitbox import HitBox
        
        self.x = x
        self.y = y
        self.size = size
        
        # Create circular hitbox centered on the gravestone
        # Radius is half the size for proper collision detection
        self.hit_box = HitBox(x, y, size // 2, 0)
        
        # Load gravestone sprite using ResourceManager
        self._load_sprite()
    
    def _load_sprite(self) -> None:
        """
        Load the gravestone sprite from resources.
        
        Uses the ResourceManager to load and cache the sprite.
        If loading fails, sprite will be None and fallback rendering
        will be used.
        """
        from src.managers.resource_manager import resource_manager
        
        try:
            self.sprite = resource_manager.load_image(
                "gravestone.png", 
                scale=(self.size, self.size)
            )
        except Exception as e:
            print(f"Warning: Could not load gravestone sprite: {e}")
            self.sprite = None
    
    def update_position(self, x: float, y: float) -> None:
        """
        Update the gravestone's position.
        
        This method updates both the gravestone's position and its
        associated hitbox to maintain collision detection accuracy.
        
        Args:
            x: New X position
            y: New Y position
        """
        self.x = x
        self.y = y
        self.hit_box.update_position(x, y)
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Render the gravestone on the screen.
        
        If a sprite is loaded, it will be rendered. Otherwise, a simple
        rectangular placeholder will be drawn (fallback rendering).
        
        Args:
            screen: Pygame surface to draw on
        """
        if self.sprite:
            # Draw the loaded sprite
            screen.blit(self.sprite, (int(self.x), int(self.y)))
        else:
            # Fallback: Draw a simple rectangular gravestone
            self._draw_fallback(screen)
    
    def _draw_fallback(self, screen: pygame.Surface) -> None:
        """
        Draw a simple rectangular gravestone as fallback.
        
        Used when the sprite cannot be loaded. Renders a gray rectangle
        with a lighter border to represent the gravestone.
        
        Args:
            screen: Pygame surface to draw on
        """
        rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)
        
        # Draw filled rectangle (body)
        pygame.draw.rect(screen, self.FALLBACK_COLOR_DARK, rect)
        
        # Draw border (outline)
        pygame.draw.rect(
            screen, 
            self.FALLBACK_COLOR_LIGHT, 
            rect, 
            self.FALLBACK_BORDER_WIDTH
        )
    
    def __repr__(self) -> str:
        """
        String representation for debugging.
        
        Returns:
            String showing gravestone position and size
        """
        return f"Gravestone(x={self.x:.1f}, y={self.y:.1f}, size={self.size})"
