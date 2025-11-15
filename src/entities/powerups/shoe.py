"""
Power-up: Buty - zwiększają prędkość gracza.
"""
import pygame
from src.entities.powerups.base_powerup import BasePowerUp
from src.managers.resource_manager import resource_manager
from src.core.constants import POWERUP_SIZE, SPEED_BOOST_CHARGES


class Shoe(BasePowerUp):
    """Power-up: Buty - podwajają prędkość gracza na 5 sekund."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, POWERUP_SIZE)
    
    def _load_sprite(self):
        """Ładuje sprite butów."""
        self.sprite = resource_manager.load_image("boost_shoe2.png", 
                                                   scale=(self.size, self.size))
        if self.sprite is None:
            # Fallback - żółty kwadrat
            self.sprite = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            self.sprite.fill((220, 200, 60))
    
    def get_name(self) -> str:
        return "shoe"
    
    def get_charges(self) -> int:
        return SPEED_BOOST_CHARGES
