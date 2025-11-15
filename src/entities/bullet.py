"""
Klasa pocisku wystrzeliwanego przez gracza.
"""
import pygame
import math
from typing import TYPE_CHECKING
from src.utils.hitbox import HitBox
from src.core.constants import BULLET_SIZE, URANEK_FRAME_WIDTH, URANEK_FRAME_HEIGHT, URANEK_SCALE
from src.managers.resource_manager import resource_manager

if TYPE_CHECKING:
    from src.entities.player import Player


class Bullet:
    """Pocisk gracza (fireball)."""
    
    def __init__(self, player: 'Player', target_x: float, target_y: float, 
                 strength_active: bool = False):
        # Spawn bullet w centrum gracza
        player_width = URANEK_FRAME_WIDTH * URANEK_SCALE
        player_height = URANEK_FRAME_HEIGHT * URANEK_SCALE
        self.x = player.x + player_width / 2
        self.y = player.y + player_height / 2
        
        # Obrażenia (podwojone jeśli aktywna siła)
        self.ad = 20 if strength_active else 10
        
        # Oblicz kierunek
        dx = target_x - self.x
        dy = target_y - self.y
        normalize_factor = math.sqrt(dx ** 2 + dy ** 2)
        
        if normalize_factor == 0:
            normalize_factor = 1
        
        self.vx = dx / normalize_factor
        self.vy = dy / normalize_factor
        self.angle = math.atan2(self.vy, self.vx)
        
        self.r = BULLET_SIZE
        self.movement = 10
        self.hit_box = HitBox(self.x, self.y, URANEK_FRAME_WIDTH // 4, 10)
        
        # Animacja
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 10
        self.frames = self._load_fireball_animation()
        self.current_sprite = self.frames[0] if self.frames else None
    
    def _load_fireball_animation(self) -> list:
        """Ładuje animację fireball."""
        frame_width = 150
        frame_height = 100
        scale = 0.5
        
        frames = resource_manager.load_spritesheet(
            "fireball.png", 
            frame_width, 
            frame_height,
            scale=(int(frame_width * scale), int(frame_height * scale))
        )
        
        if not frames:
            return []
        
        # Obróć klatki zgodnie z kierunkiem lotu
        angle_degrees = math.degrees(-self.angle)
        rotated_frames = []
        for frame in frames:
            rotated = pygame.transform.rotate(frame, angle_degrees)
            rotated_frames.append(rotated)
        
        return rotated_frames
    
    def update(self):
        """Aktualizuje pozycję i animację pocisku."""
        self.x += self.vx * self.movement
        self.y += self.vy * self.movement
        self.hit_box.update_position(self.x, self.y)
        
        # Animacja
        self.frame_timer += 1
        if self.frame_timer >= self.frame_speed and self.frames:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.current_sprite = self.frames[self.frame_index]
    
    def draw(self, screen: pygame.Surface):
        """Rysuje pocisk."""
        if self.current_sprite:
            sprite_rect = self.current_sprite.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.current_sprite, sprite_rect)
        else:
            # Fallback - prosty fireball
            self._draw_simple_fireball(screen)
    
    def _draw_simple_fireball(self, screen: pygame.Surface):
        """Rysuje prosty fireball jako fallback."""
        pulse = math.sin(self.frame_index * 0.5) * 0.3 + 0.7
        
        # Zewnętrzna poświata
        glow_size = int(self.r * 2.5 * pulse)
        glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 100, 0, 80), 
                         (glow_size, glow_size), glow_size)
        screen.blit(glow_surface, (int(self.x) - glow_size, int(self.y) - glow_size))
        
        # Środkowa warstwa
        pygame.draw.circle(screen, (255, 150, 0), (int(self.x), int(self.y)), 
                         int(self.r * 1.5 * pulse))
        
        # Rdzeń
        pygame.draw.circle(screen, (255, 255, 100), (int(self.x), int(self.y)), 
                         int(self.r * pulse))
        
        # Centrum
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 
                         max(2, int(self.r * 0.5)))
