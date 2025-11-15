"""
Power-up manager for handling player power-ups and their activation.
Manages speed boost, shield, and strength power-ups.
"""
import pygame
from src.ui.notification import Notification
from src.core.constants import FPS


class PowerUpManager:
    """Manages all power-up states and activations."""
    
    def __init__(self):
        # Power-up charges
        self.speed_boost_charges = 0
        self.shield_charges = 0
        self.strength_charges = 0
        
        # Active timers
        self.speed_boost_timer = 0
        self.shield_timer = 0
        self.strength_timer = 0
        
        # Previous key states for edge detection
        self._prev_e_pressed = False
        self._prev_r_pressed = False
        self._prev_t_pressed = False
        
        # Original values for restoration
        self.original_movement = None
        self.original_ad = None
    
    def add_speed_charges(self, amount: int = 3):
        """Add speed boost charges."""
        self.speed_boost_charges += amount
    
    def add_shield_charges(self, amount: int = 3):
        """Add shield charges."""
        self.shield_charges += amount
    
    def add_strength_charges(self, amount: int = 2):
        """Add strength charges."""
        self.strength_charges += amount
    
    def activate_speed_boost(self, player, notifications, font):
        """
        Activate speed boost if available.
        
        Args:
            player: Player instance to modify
            notifications: List to append notification to
            font: Pygame font for notification
            
        Returns:
            True if activated, False otherwise
        """
        if self.speed_boost_timer <= 0 and self.speed_boost_charges > 0:
            if self.original_movement is None:
                self.original_movement = player.movement
            player.movement = int(self.original_movement * 2)
            self.speed_boost_timer = FPS * 5  # 5 seconds
            self.speed_boost_charges -= 1
            notifications.append(Notification(player.x, player.y, "Speed x2! (5s)", "yellow", font))
            return True
        return False
    
    def activate_shield(self, player, notifications, font):
        """
        Activate shield if available.
        
        Args:
            player: Player instance
            notifications: List to append notification to
            font: Pygame font for notification
            
        Returns:
            True if activated, False otherwise
        """
        if self.shield_timer <= 0 and self.shield_charges > 0:
            self.shield_timer = FPS * 3  # 3 seconds
            self.shield_charges -= 1
            notifications.append(Notification(player.x, player.y, "Tarcza! (3s)", "cyan", font))
            return True
        return False
    
    def activate_strength(self, player, notifications, font):
        """
        Activate strength boost if available.
        
        Args:
            player: Player instance to modify
            notifications: List to append notification to
            font: Pygame font for notification
            
        Returns:
            True if activated, False otherwise
        """
        if self.strength_timer <= 0 and self.strength_charges > 0:
            self.original_ad = player.ad
            player.ad *= 2  # Double attack damage
            self.strength_timer = FPS * 3  # 3 seconds
            self.strength_charges -= 1
            notifications.append(Notification(player.x, player.y, "Siła x2! (3s)", "red", font))
            return True
        return False
    
    def handle_input(self, keys, player, notifications, font):
        """
        Handle power-up activation input.
        
        Args:
            keys: Pygame key state array
            player: Player instance
            notifications: List to append notifications to
            font: Pygame font for notifications
        """
        # E key - Speed boost
        e_pressed = keys[pygame.K_e]
        if e_pressed and not self._prev_e_pressed:
            self.activate_speed_boost(player, notifications, font)
        self._prev_e_pressed = e_pressed
        
        # R key - Shield
        r_pressed = keys[pygame.K_r]
        if r_pressed and not self._prev_r_pressed:
            self.activate_shield(player, notifications, font)
        self._prev_r_pressed = r_pressed
        
        # T key - Strength
        t_pressed = keys[pygame.K_t]
        if t_pressed and not self._prev_t_pressed:
            self.activate_strength(player, notifications, font)
        self._prev_t_pressed = t_pressed
    
    def update_timers(self, player, notifications, font):
        """
        Update power-up timers and handle expiration.
        
        Args:
            player: Player instance to restore values
            notifications: List to append notifications to
            font: Pygame font for notifications
        """
        # Speed boost timer
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer == 0 and self.original_movement is not None:
                player.movement = self.original_movement
                notifications.append(Notification(player.x, player.y, "Speed boost ended", "white", font))
                self.original_movement = None
        
        # Shield timer
        if self.shield_timer > 0:
            self.shield_timer -= 1
            if self.shield_timer == 0:
                notifications.append(Notification(player.x, player.y, "Tarcza wygasła", "white", font))
        
        # Strength timer
        if self.strength_timer > 0:
            self.strength_timer -= 1
            if self.strength_timer == 0 and self.original_ad is not None:
                player.ad = self.original_ad
                notifications.append(Notification(player.x, player.y, "Siła wygasła", "white", font))
                self.original_ad = None
    
    def is_shield_active(self) -> bool:
        """Check if shield is currently active."""
        return self.shield_timer > 0
    
    def is_strength_active(self) -> bool:
        """Check if strength boost is currently active."""
        return self.strength_timer > 0
    
    def reset(self, keep_charges: bool = False):
        """
        Reset power-up manager.
        
        Args:
            keep_charges: If True, preserve charge counts (for level transitions)
        """
        if not keep_charges:
            self.speed_boost_charges = 0
            self.shield_charges = 0
            self.strength_charges = 0
        
        self.speed_boost_timer = 0
        self.shield_timer = 0
        self.strength_timer = 0
        
        self._prev_e_pressed = False
        self._prev_r_pressed = False
        self._prev_t_pressed = False
        
        self.original_movement = None
        self.original_ad = None
    
    def get_charges(self) -> dict:
        """
        Get current charge counts.
        
        Returns:
            Dictionary with charge counts for each power-up type
        """
        return {
            'speed': self.speed_boost_charges,
            'shield': self.shield_charges,
            'strength': self.strength_charges
        }
    
    def set_charges(self, speed: int = 0, shield: int = 0, strength: int = 0):
        """
        Set charge counts.
        
        Args:
            speed: Speed boost charges
            shield: Shield charges
            strength: Strength charges
        """
        self.speed_boost_charges = speed
        self.shield_charges = shield
        self.strength_charges = strength
    
    def draw_hud(self, screen, font, screen_height, shoe_icon=None, shield_icon=None, sword_icon=None):
        """
        Draw power-up charges HUD.
        
        Args:
            screen: Pygame screen surface
            font: Pygame font
            screen_height: Screen height in pixels
            shoe_icon: Optional shoe icon surface
            shield_icon: Optional shield icon surface
            sword_icon: Optional sword icon surface
        """
        # Speed boost
        if self.speed_boost_charges > 0:
            hud_y_offset = screen_height - 100
            if shoe_icon:
                screen.blit(shoe_icon, (20, hud_y_offset))
                speed_text = font.render(f"x{self.speed_boost_charges} (E)", True, (255, 255, 0))
                screen.blit(speed_text, (70, hud_y_offset + 5))
            else:
                speed_text = font.render(f"Buty (E): {self.speed_boost_charges}", True, (255, 255, 0))
                screen.blit(speed_text, (20, hud_y_offset))
        
        # Shield
        if self.shield_charges > 0:
            shield_y_offset = screen_height - 60
            if shield_icon:
                screen.blit(shield_icon, (20, shield_y_offset))
                shield_text = font.render(f"x{self.shield_charges} (R)", True, (100, 200, 255))
                screen.blit(shield_text, (70, shield_y_offset + 5))
            else:
                shield_text = font.render(f"Tarcza (R): {self.shield_charges}", True, (100, 200, 255))
                screen.blit(shield_text, (20, shield_y_offset))
        
        # Strength
        if self.strength_charges > 0:
            strength_y_offset = screen_height - 120
            if sword_icon:
                screen.blit(sword_icon, (20, strength_y_offset))
                strength_text = font.render(f"x{self.strength_charges} (T)", True, (255, 100, 100))
                screen.blit(strength_text, (70, strength_y_offset + 5))
            else:
                strength_text = font.render(f"Siła (T): {self.strength_charges}", True, (255, 100, 100))
                screen.blit(strength_text, (20, strength_y_offset))
