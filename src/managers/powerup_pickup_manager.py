"""
Power-up pickup manager for handling power-up drops and collection.
"""
import random
from src.entities.powerups.shoe import Shoe
from src.entities.powerups.shield import Shield
from src.entities.powerups.strength import Strength
from src.ui.notification import Notification


class PowerUpPickupManager:
    """Manages power-up item drops and player collection."""
    
    def __init__(self):
        """Initialize power-up pickup manager."""
        self.current_item = None
        self.current_room_death_counter = 0
        self.current_room_drop_index = None
        self.dropped_this_level = False
        self.last_powerup_type = None
    
    def reset_for_new_level(self):
        """Reset state for a new level."""
        self.current_item = None
        self.current_room_death_counter = 0
        self.current_room_drop_index = None
        self.dropped_this_level = False
    
    def reset_for_new_room(self):
        """Reset state for a new room."""
        self.current_room_death_counter = 0
        self.current_room_drop_index = None
    
    def handle_enemy_death(self, enemy):
        """
        Handle potential power-up drop when an enemy dies.
        
        Args:
            enemy: The enemy that died
            
        Returns:
            True if a power-up was dropped, False otherwise
        """
        self.current_room_death_counter += 1
        
        # Boss-only drop: spawn a power-up only once per level
        if (not self.dropped_this_level) and self.current_item is None and getattr(enemy, 'is_boss', False):
            self._spawn_powerup(enemy.x, enemy.y)
            self.dropped_this_level = True
            self.current_room_drop_index = None
            return True
        
        return False
    
    def _spawn_powerup(self, x, y):
        """
        Spawn a random power-up at the given position.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        # Choose power-up type but avoid repeating last_powerup_type
        options = ['shoe', 'shield', 'strength']
        if self.last_powerup_type in options:
            try:
                options.remove(self.last_powerup_type)
            except ValueError:
                pass
        
        choice = random.choice(options) if options else 'shoe'
        
        if choice == 'shoe':
            self.current_item = Shoe(max(0, x), max(0, y))
        elif choice == 'shield':
            self.current_item = Shield(max(0, x), max(0, y))
        else:
            self.current_item = Strength(max(0, x), max(0, y))
    
    def update_and_draw(self, screen):
        """
        Update and draw the current power-up item.
        
        Args:
            screen: Pygame screen surface
        """
        if self.current_item:
            self.current_item.draw(screen)
    
    def check_collection(self, player, powerup_manager, notifications, font):
        """
        Check if player collected the power-up item.
        
        Args:
            player: Player instance
            powerup_manager: PowerUpManager instance to add charges
            notifications: List to append notifications to
            font: Pygame font for notifications
            
        Returns:
            True if item was collected, False otherwise
        """
        if self.current_item and player.hit_box.collide(self.current_item.hit_box):
            # Add charges based on item type
            if isinstance(self.current_item, Shoe):
                powerup_manager.add_speed_charges(3)
                self.last_powerup_type = 'shoe'
                notifications.append(Notification(player.x, player.y, "Buty! +3 ładunki (E)", "yellow", font))
            elif isinstance(self.current_item, Shield):
                powerup_manager.add_shield_charges(3)
                self.last_powerup_type = 'shield'
                notifications.append(Notification(player.x, player.y, "Tarcza! +3 ładunki (R)", "cyan", font))
            elif isinstance(self.current_item, Strength):
                powerup_manager.add_strength_charges(2)
                self.last_powerup_type = 'strength'
                notifications.append(Notification(player.x, player.y, "Siła! +2 ładunki (T)", "red", font))
            
            self.current_item = None
            return True
        
        return False
    
    def has_item(self):
        """
        Check if there's a current power-up item.
        
        Returns:
            True if item exists, False otherwise
        """
        return self.current_item is not None
