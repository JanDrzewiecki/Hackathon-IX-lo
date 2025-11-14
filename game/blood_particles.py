import pygame
import math
import random

class BloodParticle:
    """Single blood particle"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Random velocity for explosion effect
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        # Gravity effect
        self.gravity = 0.3
        # Size and color
        self.size = random.randint(3, 7)
        self.life = random.randint(30, 60)  # Frames to live
        self.max_life = self.life
        # Green blood color variations
        green_intensity = random.randint(180, 255)
        self.color = (0, green_intensity, random.randint(0, 50))

    def update(self):
        """Update particle position and life"""
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity  # Apply gravity
        self.vx *= 0.98  # Air resistance
        self.life -= 1

    def draw(self, screen):
        """Draw particle with fade effect"""
        if self.life > 0:
            # Calculate alpha based on remaining life
            alpha = int(255 * (self.life / self.max_life))
            # Create surface with alpha
            particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)

            # Draw particle with glow effect
            for i in range(2):
                glow_size = self.size + i * 2
                glow_alpha = alpha // (i + 1)
                r, g, b = self.color
                pygame.draw.circle(particle_surface, (r, g, b, glow_alpha),
                                 (self.size, self.size), glow_size)

            screen.blit(particle_surface, (int(self.x) - self.size, int(self.y) - self.size))


class BloodParticleSystem:
    """Manages multiple blood particles"""
    def __init__(self, x, y, num_particles=20):
        self.particles = []
        # Create explosion of particles
        for _ in range(num_particles):
            self.particles.append(BloodParticle(x, y))

    def update(self):
        """Update all particles"""
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)

    def is_alive(self):
        """Check if any particles are still alive"""
        return len(self.particles) > 0

