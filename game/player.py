import pygame
from settings import *
from hit_box import *

class Player:
    def __init__(self, player_start_x, player_start_y):
        self.x = player_start_x
        self.y = player_start_y
        self.hp = 60
        self.ad = 20
        self.movement = 8
        self.points = 0
        self.hit_box = HitBox(self.x, self.y, PLAYER_SIZE // 2 - 2, PLAYER_SIZE // 2)
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 6
        self.frames = self.load_sheet("uranek.png", PLAYER_SIZE, PLAYER_SIZE)
        self.current_sprite = self.frames[0]

    def load_sheet(self, path, frame_width, frame_height):
        sheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()

        cols = sheet_width // frame_width
        frames = []

        for col in range(cols):
            rect = pygame.Rect(col * frame_width,0,frame_width,frame_height)
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), rect)

            frame = pygame.transform.scale(frame, URANEK_SIZE)

            frames.append(frame)

        return frames

    def update(self, keys):
        moving = False

        if keys[pygame.K_a] and self.x - PLAYER_SIZE >= 0:
            self.x -= self.movement
            moving = True

        if keys[pygame.K_d] and self.x + PLAYER_SIZE <= SCREEN_WIDTH:
            self.x += self.movement
            moving = True

        if keys[pygame.K_w] and self.y - PLAYER_SIZE >= 0:
            self.y -= self.movement
            moving = True

        if keys[pygame.K_s] and self.y + PLAYER_SIZE <= SCREEN_HEIGHT:
            self.y += self.movement
            moving = True

        if moving:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_speed:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
        else:
            self.frame_index = 0

        self.current_sprite = self.frames[self.frame_index]
        self.hit_box.update_position(self.x, self.y)

    def draw(self, screen):
        screen.blit(self.current_sprite, (self.x, self.y))