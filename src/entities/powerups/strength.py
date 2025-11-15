"""
Power-up: Siła - podwaja obrażenia gracza.
"""
import pygame
from src.entities.powerups.base_powerup import BasePowerUp
from src.managers.resource_manager import resource_manager
from src.core.constants import POWERUP_SIZE, STRENGTH_CHARGES


class Strength(BasePowerUp):
    """Power-up: Siła - podwaja obrażenia gracza na 3 sekundy."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, POWERUP_SIZE)
    
    def _load_sprite(self):
        """Ładuje sprite miecza."""
        sprite_names = ["swordbg.png", "sword.png"]
        
        for name in sprite_names:
            self.sprite = resource_manager.load_image(name, scale=(self.size, self.size))
            if self.sprite:
                break
        
        if self.sprite is None:
            # Fallback - prostokąt przypominający miecz
            self.sprite = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(self.sprite, (180, 180, 180), 
                           (self.size // 3, 4, self.size // 6, self.size - 8))
            pygame.draw.polygon(self.sprite, (200, 200, 200), 
                              [(self.size // 2, 0), 
                               (self.size // 2 - 6, 8), 
                               (self.size // 2 + 6, 8)])
    
    def get_name(self) -> str:
        return "strength"
    
    def get_charges(self) -> int:
        return STRENGTH_CHARGES
