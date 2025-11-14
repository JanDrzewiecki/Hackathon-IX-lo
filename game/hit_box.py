import  pygame
from settings import*

class HitBox:
    def __init__(self, x, y, r, size_offset):
        self.x = x + size_offset
        self.y = y + size_offset
        self.r = r
        self.size_offset = size_offset

    def update_position(self, x, y):
        self.x = x + self.size_offset
        self.y = y + self.size_offset


    def collide(self, other: "HitBox"):
        distance_sq = (self.x - other.x) ** 2 + (self.y - other.y) ** 2
        return distance_sq <= (self.r + other.r) ** 2