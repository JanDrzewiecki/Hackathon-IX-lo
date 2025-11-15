"""
Enemy bullet manager for handling enemy projectiles and their collisions.
"""
import pygame


class EnemyBulletManager:
    """Manages enemy bullets including updates, collisions, and rendering."""
    
    def __init__(self, screen_width: int, screen_height: int, fps: int):
        """
        Initialize enemy bullet manager.
        
        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
            fps: Frames per second for damage cooldown timing
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = fps
        
        self.enemy_bullets = []
        self.damage_cooldown = 0
    
    def clear(self):
        """Clear all enemy bullets."""
        self.enemy_bullets.clear()
        self.damage_cooldown = 0
    
    def add_bullet(self, bullet):
        """
        Add an enemy bullet to the manager.
        
        Args:
            bullet: EnemyBullet instance to add
        """
        self.enemy_bullets.append(bullet)
    
    def get_bullets(self):
        """
        Get the list of enemy bullets.
        
        Returns:
            List of enemy bullets
        """
        return self.enemy_bullets
    
    def update_and_draw(self, screen, player, powerup_manager):
        """
        Update and draw all enemy bullets, handle collisions with player.
        
        Args:
            screen: Pygame screen surface
            player: Player instance
            powerup_manager: PowerUpManager instance for shield checking
        """
        for eb in self.enemy_bullets[:]:
            eb.update()
            eb.draw(screen)
            
            # Remove if off-screen
            if eb.x < 0 or eb.x > self.screen_width or eb.y < 0 or eb.y > self.screen_height:
                self.enemy_bullets.remove(eb)
            # Check collision with player
            elif player.hit_box.collide(eb.hit_box):
                if powerup_manager.is_shield_active():
                    # Shield blocks the bullet
                    self.enemy_bullets.remove(eb)
                elif self.damage_cooldown <= 0:
                    # Deal damage to player
                    player.hp = max(0, player.hp - eb.ad)
                    self.damage_cooldown = int(self.fps * 0.75)
                    self.enemy_bullets.remove(eb)
        
        # Update damage cooldown
        self.damage_cooldown = max(0, self.damage_cooldown - 1)
    
    def get_damage_cooldown(self):
        """
        Get current damage cooldown value.
        
        Returns:
            Current damage cooldown in frames
        """
        return self.damage_cooldown
