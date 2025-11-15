"""
Boss HP bar manager for displaying animated boss health bars.
"""
import pygame
from src.core.constants import FPS


class BossBarManager:
    """Manages the boss HP bar display with intro animation."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize boss bar manager.
        
        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Boss bar state
        self.active = False
        self.target_enemy = None
        
        # Animation state
        self.intro_timer = 0
        self.intro_duration = int(FPS * 1.0)  # 1 second intro animation
        self.intro_progress = 0.0
    
    def activate(self, enemy, notifications=None, font=None, player_x=0, player_y=0):
        """
        Activate boss bar for a specific enemy.
        
        Args:
            enemy: Enemy instance to track
            notifications: Optional list to add "BOSS!" notification
            font: Optional font for notification
            player_x: Player X position for notification
            player_y: Player Y position for notification
        """
        self.active = True
        self.target_enemy = enemy
        self.intro_timer = self.intro_duration
        self.intro_progress = 0.0
        
        # Add notification if provided
        if notifications is not None and font is not None:
            from src.ui.notification import Notification
            notifications.append(Notification(player_x, player_y, "BOSS!", "red", font))
    
    def deactivate(self):
        """Deactivate the boss bar."""
        self.active = False
        self.target_enemy = None
        self.intro_timer = 0
        self.intro_progress = 0.0
    
    def update(self, enemies):
        """
        Update boss bar state.
        
        Args:
            enemies: List of current enemies
            
        Returns:
            True if boss bar is still active, False if deactivated
        """
        if not self.active or self.target_enemy is None:
            return False
        
        # Check if boss is still alive
        if self.target_enemy not in enemies:
            self.deactivate()
            return False
        
        return True
    
    def draw(self, screen, enemies):
        """
        Draw the boss HP bar with animation.
        
        Args:
            screen: Pygame screen surface
            enemies: List of current enemies (to check if boss is alive)
        """
        if not self.active or self.target_enemy is None:
            return
        
        # Check if boss died or was removed
        if self.target_enemy not in enemies:
            self.deactivate()
            return
        
        # Bar dimensions and position
        bar_width = int(self.screen_width * 0.78)
        bar_height = max(20, int(self.screen_height * 0.05))
        margin_bottom = 24
        x_bar = (self.screen_width - bar_width) // 2
        y_target = self.screen_height - margin_bottom - bar_height
        
        # Intro animation: slide up from offscreen and fade in
        if self.intro_timer > 0:
            self.intro_progress = 1.0 - (self.intro_timer / self.intro_duration)
            # Smoothstep easing
            eased = self.intro_progress * self.intro_progress * (3 - 2 * self.intro_progress)
            y = self.screen_height + int(bar_height * 2 * (1.0 - eased)) - bar_height - margin_bottom
            alpha = int(255 * eased)
            self.intro_timer -= 1
        else:
            y = y_target
            alpha = 255
        
        # Draw background strip
        bg_rect = pygame.Rect(x_bar - 6, y - 6, bar_width + 12, bar_height + 12)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((20, 20, 20, alpha))
        screen.blit(bg_surface, (bg_rect.x, bg_rect.y))
        
        # Inner bar background
        inner_rect = pygame.Rect(x_bar, y, bar_width, bar_height)
        inner_surface = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
        inner_surface.fill((60, 60, 60, int(alpha * 0.95)))
        screen.blit(inner_surface, (inner_rect.x, inner_rect.y))
        
        # Calculate HP fill
        shown_hp = max(0, min(self.target_enemy.hp, self.target_enemy.max_hp))
        fill_ratio = (shown_hp / float(self.target_enemy.max_hp)) if self.target_enemy.max_hp > 0 else 0.0
        fill_w = max(0, int(bar_width * fill_ratio))
        
        # Color based on HP percentage
        if fill_ratio > 0.5:
            color = (50, 205, 50)  # Green
        elif fill_ratio > 0.25:
            color = (255, 215, 0)  # Yellow/Gold
        else:
            color = (220, 50, 50)  # Red
        
        # Draw HP fill
        if fill_w > 0:
            fill_surface = pygame.Surface((fill_w, bar_height), pygame.SRCALPHA)
            fill_surface.fill((*color, alpha))
            screen.blit(fill_surface, (x_bar, y))
        
        # Draw border
        pygame.draw.rect(screen, (200, 200, 200), inner_rect, width=2, border_radius=bar_height//2)
        
        # Draw HP text centered
        try:
            text_font = pygame.font.SysFont(None, max(20, int(bar_height * 0.6)))
            text = f"BOSS HP: {shown_hp} / {self.target_enemy.max_hp}"
            text_surf = text_font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(self.screen_width // 2, y + bar_height // 2))
            screen.blit(text_surf, text_rect)
        except Exception:
            pass  # Fail silently if font rendering fails
    
    def is_active(self) -> bool:
        """Check if boss bar is currently active."""
        return self.active
    
    def reset(self):
        """Reset boss bar state."""
        self.deactivate()
