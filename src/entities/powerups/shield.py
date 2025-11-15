"""
Power-up: Tarcza - zapewnia nieśmiertelność.
"""
import pygame
from src.entities.powerups.base_powerup import BasePowerUp
from src.managers.resource_manager import resource_manager
from src.core.constants import POWERUP_SIZE, SHIELD_CHARGES


class Shield(BasePowerUp):
    """Power-up: Tarcza - zapewnia nieśmiertelność na 3 sekundy."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, POWERUP_SIZE)
    
    def _load_sprite(self):
        """Ładuje sprite tarczy."""
        # Próbuj różnych ścieżek
        sprite_names = ["shield.png", "shield.jpg.avif", "boost_shield.png"]
        
        for name in sprite_names:
            self.sprite = resource_manager.load_image(name, scale=(self.size, self.size))
            if self.sprite:
                break
        
        if self.sprite is None:
            # Fallback - niebieski okrąg
            self.sprite = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(self.sprite, (80, 160, 255), 
                             (self.size // 2, self.size // 2), self.size // 2)
            pygame.draw.circle(self.sprite, (200, 230, 255), 
                             (self.size // 2, self.size // 2), self.size // 2, 3)
    
    def get_name(self) -> str:
        return "shield"
    
    def get_charges(self) -> int:
        return SHIELD_CHARGES
