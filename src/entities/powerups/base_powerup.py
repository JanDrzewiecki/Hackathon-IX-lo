"""
Bazowa klasa dla power-upów w grze.
"""
import pygame
from abc import ABC, abstractmethod
from src.utils.hitbox import HitBox
from src.managers.resource_manager import resource_manager


class BasePowerUp(ABC):
    """Abstrakcyjna klasa bazowa dla wszystkich power-upów."""
    
    def __init__(self, x: float, y: float, size: int = 48):
        self.x = x
        self.y = y
        self.size = size
        self.alive = True
        self.sprite: pygame.Surface = None
        self.hit_box = HitBox(self.x, self.y, r=20, size_offset=size // 2)
        self._load_sprite()
    
    @abstractmethod
    def _load_sprite(self):
        """Ładuje sprite power-upu. Musi być zaimplementowane w podklasach."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Zwraca nazwę power-upu."""
        pass
    
    @abstractmethod
    def get_charges(self) -> int:
        """Zwraca ilość ładunków jakie daje power-up."""
        pass
    
    def update_position(self, x: float, y: float):
        """Aktualizuje pozycję power-upu."""
        self.x = x
        self.y = y
        self.hit_box.update_position(x, y)
    
    def draw(self, screen: pygame.Surface):
        """Rysuje power-up."""
        if not self.alive:
            return
        
        if self.sprite:
            screen.blit(self.sprite, (int(self.x), int(self.y)))
        else:
            # Fallback - kolorowy kwadrat
            pygame.draw.rect(screen, (255, 0, 255), 
                           (int(self.x), int(self.y), self.size, self.size))
    
    def collect(self) -> dict:
        """
        Zbiera power-up.
        
        Returns:
            Słownik z informacjami o zebranym power-upie
        """
        self.alive = False
        return {
            'name': self.get_name(),
            'charges': self.get_charges()
        }
