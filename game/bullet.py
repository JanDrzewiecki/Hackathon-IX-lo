import pygame
import math
from settings import *
from hit_box import *

class Bullet:
    def __init__(self, player, target_x, target_y):
        # Spawn bullet at center of player sprite
        player_width = URANEK_FRAME_WIDTH * 0.7  # skale = 0.7
        player_height = URANEK_FRAME_HEIGHT * 0.7
        self.x = player.x + player_width / 2
        self.y = player.y + player_height / 2
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
        self.hit_box = HitBox(self.x, self.y, URANEK_FRAME_WIDTH // 4, ENEMY_SIZE // 2)

        # Animation properties
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 10  # Speed of animation (higher = slower, smoother)

        # Calculate angle for rotation (direction of bullet)
        self.angle = math.atan2(self.vy, self.vx)

        # Load fireball sprite sheet
        self.fireball_frame_width = 150  # Width of each frame in the sprite sheet
        self.fireball_frame_height = 100  # Height of each frame
        self.fireball_scale = 0.5  # Scale factor for the fireball
        self.frames = self.load_sheet("fireball.png", self.fireball_frame_width, self.fireball_frame_height)
        self.current_sprite = self.frames[0] if self.frames else None

    def load_sheet(self, path, frame_width, frame_height):
        """Load sprite sheet and split it into individual frames"""
        try:
            sheet = pygame.image.load(path).convert_alpha()
            sheet_width, sheet_height = sheet.get_size()

            cols = sheet_width // frame_width
            frames = []

            for col in range(cols):
                rect = pygame.Rect(col * frame_width, 0, frame_width, frame_height)
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), rect)

                # Scale the frame
                scaled_size = (int(frame_width * self.fireball_scale), int(frame_height * self.fireball_scale))
                frame = pygame.transform.scale(frame, scaled_size)

                # Rotate frame to match bullet direction
                angle_degrees = math.degrees(-self.angle)
                frame = pygame.transform.rotate(frame, angle_degrees)

                frames.append(frame)

            return frames
        except Exception as e:
            print(f"Error loading fireball sprite: {e}")
            return []

    def draw(self, screen):
        """Draw the animated fireball sprite"""
        if self.current_sprite:
            # Get the rect for centering
            sprite_rect = self.current_sprite.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.current_sprite, sprite_rect)
        else:
            # Fallback: draw simple animated fireball if sprite didn't load
            self.draw_simple_fireball(screen)

    def draw_simple_fireball(self, screen):
        """Draw a simple fireball when sprite is not available"""
        # Pulsing effect
        import math
        pulse = math.sin(self.frame_index * 0.5) * 0.3 + 0.7

        # Outer glow
        glow_size = int(self.r * 2.5 * pulse)
        glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 100, 0, 80), (glow_size, glow_size), glow_size)
        screen.blit(glow_surface, (int(self.x) - glow_size, int(self.y) - glow_size))

        # Middle layer
        middle_size = int(self.r * 1.5 * pulse)
        pygame.draw.circle(screen, (255, 150, 0), (int(self.x), int(self.y)), middle_size)

        # Inner core
        core_size = int(self.r * pulse)
        pygame.draw.circle(screen, (255, 255, 100), (int(self.x), int(self.y)), core_size)

        # Center
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), max(2, int(self.r * 0.5)))

    def update(self, bullets: list["Bullet"]):
        """Update bullet position and animation"""
        # Update position
        self.x += self.vx * self.movement
        self.y += self.vy * self.movement
        self.hit_box.update_position(self.x, self.y)

        # Update animation
        self.update_animation()

    def update_animation(self):
        """Update the animation frame"""
        self.frame_timer += 1
        if self.frame_timer >= self.frame_speed:
            self.frame_timer = 0
            if self.frames:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.current_sprite = self.frames[self.frame_index]