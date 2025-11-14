import  pygame
from settings import*
from hit_box import*

class Enemy:
    def __init__(self, x, y, room=None):
        self.x = x
        self.y = y
        self.hp = 50
        self.ad = 10
        self.movement = 2
        self.hit_box = HitBox(self.x, self.y, PLAYER_SIZE//2 - 2, PLAYER_SIZE//2)
        self.room = room

    def set_room(self, room):
        """Set the room boundaries for this enemy."""
        self.room = room

    def draw(self, screen):
        pygame.draw.rect(screen, "red", (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))

    def update(self, player_x, player_y):
        #calculating direction to the player
        vx = self.x - player_x
        vy = self.y - player_y
        normalize_factor = (vx ** 2 + vy ** 2) ** 0.5

        # Avoid division by zero when enemy is at same position as player
        if normalize_factor == 0:
            return

        vx /= normalize_factor
        vy /= normalize_factor
        #updating position
        new_x = self.x - vx * self.movement
        new_y = self.y - vy * self.movement

        # Clamp position to room boundaries if room is set
        if self.room:
            new_x, new_y = self.room.clamp_position(new_x, new_y, PLAYER_SIZE)

        self.x = new_x
        self.y = new_y
        self.hit_box.update_position(self.x, self.y)
