from player import*

class Bullet:
    def __init__(self, player, target_x, target_y):
        self.x = player.x
        self.y = player.y
        self.tx = target_x
        self.ty = target_y
        self.ad = 10  # Changed from 100 to 10 for balanced gameplay
        self.vx = self.tx - self.x
        self.vy = self.ty - self.y
        normalize_factor = (self.vx ** 2 + self.vy ** 2) ** 0.5
        self.vx /= normalize_factor
        self.vy /= normalize_factor
        self.r = BULLET_SIZE
        self.movement = 10
        self.hit_box = HitBox(self.x, self.y, URANEK_FRAME_WIDTH // 4,ENEMY_SIZE // 2 )

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.r)

    def update(self, bullets: list["Bullet"]):

        self.x += self.vx * self.movement
        self.y += self.vy * self.movement
        self.hit_box.update_position(self.x,self.y)

