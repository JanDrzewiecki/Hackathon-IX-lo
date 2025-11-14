import  pygame
from settings import*

class Notification:

    def __init__(self, x, y, value, color, font):
        self.x = x
        self.y = y
        self.value = value
        self.color = color
        self.timer = FPS * 2
        self.count = 0
        self.step = FPS
        self.font = font

    def draw(self, screen):
        text = self.font.render(str(self.value), True, self.color)
        screen.blit(text, (self.x, self.y))

    def update(self, notifications: list["Notification"]):
            self.count += 1
            if self.timer/2 > self.count:
                self.y -= 1
            elif self.count == self.timer:
                notifications.remove(self)
            elif self.count > self.timer/2:
                self.y += 1