import  pygame
from settings import*
from hit_box import*

class Player:
    def __init__(self, start_x=None, start_y=None):
        # Use provided position or default to center of screen
        self.x = start_x if start_x is not None else SCREEN_WIDTH // 2
        self.y = start_y if start_y is not None else SCREEN_HEIGHT // 2
        self.hp = 200
        self.ad = 20
        self.movement = 50
        self.hit_box = HitBox(self.x, self.y, PLAYER_SIZE//2 - 2, PLAYER_SIZE//2)
        self.points = 0

    def draw(self, screen):
        pygame.draw.rect(screen, "white", (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))

    def update(self):
        self.hit_box.update_position(self.x,self.y)