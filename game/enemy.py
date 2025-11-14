import  pygame
from settings import*
from hit_box import*

class Enemy:
    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.hp = 50
        self.ad = 10
        self.movement = 2
        self.hit_box = HitBox(self.x, self.y, PLAYER_SIZE//2 - 2,PLAYER_SIZE//2)

    def draw(self, screen):
        pygame.draw.rect(screen, "red", (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))

    def update(self, player_x, player_y):
        #calculating direction to the player
        vx = self.x - player_x
        vy = self.y - player_y
        normalize_factor = (vx ** 2 + vy ** 2) ** 0.5
        vx /= normalize_factor
        vy /= normalize_factor
        #updating position
        self.x -= vx * self.movement
        self.y -= vy * self.movement
        self.hit_box.update_position(self.x,self.y)