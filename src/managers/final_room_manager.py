"""
Final Room Manager - Single room with final boss for level 4 (after killing 3 bosses)
"""
import pygame
from src.entities.enemy_type import EnemyType
from src.core.constants import *


class FinalRoomNode:
    """Single room for final boss"""
    def __init__(self):
        self.room_id = 0
        self.connections = {
            'top': None,
            'bottom': None,
            'left': None,
            'right': None
        }
        self.enemy_type = EnemyType.FINAL_BOSS


class FinalRoomManager:
    """Manages a single room with the final boss for level 4 (after beating 3 regular bosses)"""

    def __init__(self, screen_width, screen_height, margin_pixels=100):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.margin = margin_pixels

        # Calculate room dimensions (centered on screen)
        self.room_width = screen_width - 2 * margin_pixels
        self.room_height = screen_height - 2 * margin_pixels
        self.room_x = margin_pixels
        self.room_y = margin_pixels

        # Single room with final boss
        self.rooms = [FinalRoomNode()]
        self.current_room_id = 0
        self.current_room = self.rooms[0]

        # No corridors initially (exit corridor appears after boss is killed)
        self.corridors = []
        self.exit_corridor = None
        self.exit_corridor_open = False

        # Door animation (for exit)
        self.door_opening_progress = 0.0
        self.door_fully_open = False

        # Load gate image for exit corridor
        try:
            self.gate_image = pygame.image.load("game/gate.png").convert_alpha()
        except:
            try:
                self.gate_image = pygame.image.load("gate.png").convert_alpha()
            except:
                self.gate_image = None
                print("Warning: Could not load gate.png")

        # Load doors sprite sheet
        try:
            self.doors_spritesheet = pygame.image.load("game/doors.png").convert_alpha()
        except:
            try:
                self.doors_spritesheet = pygame.image.load("doors.png").convert_alpha()
            except:
                self.doors_spritesheet = None
                print("Warning: Could not load doors.png")

        # Door animation configuration
        self.door_frame_count = 5
        if self.doors_spritesheet:
            total_width = self.doors_spritesheet.get_width()
            self.door_sprite_height = self.doors_spritesheet.get_height()
            self.door_sprite_width = total_width // self.door_frame_count

        # Load final-map.png as background for the room
        try:
            self.background_image = pygame.image.load("game/final-map.png").convert()
        except:
            try:
                self.background_image = pygame.image.load("final-map.png").convert()
            except:
                self.background_image = None
                print("Warning: Could not load final-map.png")

        # Scale background to fit the room
        if self.background_image:
            self.background_image = pygame.transform.scale(self.background_image,
                                                          (self.room_width, self.room_height))

    def create_exit_corridor(self):
        """Create the exit corridor after final boss is defeated"""
        self.exit_corridor_open = True
        self.door_opening_progress = 0.0
        # Exit is at the top of the room
        corridor_width = 300
        self.exit_corridor = {
            'position': 'top',
            'x': self.room_x + self.room_width // 2 - corridor_width // 2,
            'y': 0,
            'width': corridor_width,
            'height': self.room_y
        }

    def update_door_animation(self, room_cleared):
        """Update door opening animation"""
        if self.exit_corridor_open and not self.door_fully_open:
            # Open doors over 0.5 seconds (30 frames at 60 FPS)
            self.door_opening_progress += 1.0 / 30.0
            if self.door_opening_progress >= 1.0:
                self.door_opening_progress = 1.0
                self.door_fully_open = True

    def draw(self, screen, final_boss_killed, room_cleared):
        """Draw the final room and exit corridor if boss is killed"""
        # Draw background image if loaded
        if self.background_image:
            screen.blit(self.background_image, (self.room_x, self.room_y))

        # Draw room border
        pygame.draw.rect(screen, (255, 255, 255),
                        (self.room_x, self.room_y, self.room_width, self.room_height), 3)

        # Draw golden exit doors if final boss is killed
        if final_boss_killed and self.exit_corridor:
            # Draw golden doors (fully open, no animation needed - it's the victory door)
            if self.gate_image and self.door_fully_open:
                # Use the last frame (fully open) from doors.png
                if self.doors_spritesheet:
                    # Get the last frame (index 4) which is fully open
                    frame_rect = pygame.Rect((self.door_frame_count - 1) * self.door_sprite_width, 0,
                                            self.door_sprite_width, self.door_sprite_height)
                    frame = self.doors_spritesheet.subsurface(frame_rect)

                    # Scale to corridor size
                    door_scaled = pygame.transform.scale(frame,
                                                         (self.exit_corridor['width'], self.exit_corridor['height']))
                    screen.blit(door_scaled, (self.exit_corridor['x'], self.exit_corridor['y']))
                else:
                    # Fallback: draw golden rectangle if spritesheet not loaded
                    pygame.draw.rect(screen, (255, 215, 0),  # Gold color
                                   (self.exit_corridor['x'], self.exit_corridor['y'],
                                    self.exit_corridor['width'], self.exit_corridor['height']))
                    pygame.draw.rect(screen, (255, 255, 255),  # White border
                                   (self.exit_corridor['x'], self.exit_corridor['y'],
                                    self.exit_corridor['width'], self.exit_corridor['height']), 5)

                # Add "VICTORY" text above the golden doors
                try:
                    victory_font = pygame.font.SysFont(None, 48)
                    victory_text = victory_font.render("VICTORY!", True, (255, 215, 0))
                    text_rect = victory_text.get_rect(center=(self.exit_corridor['x'] + self.exit_corridor['width'] // 2,
                                                             self.room_y - 40))
                    screen.blit(victory_text, text_rect)
                except:
                    pass

    def clamp_position(self, x, y, size):
        """Clamp entity position to room boundaries"""
        x = max(self.room_x, min(x, self.room_x + self.room_width - size))
        y = max(self.room_y, min(y, self.room_y + self.room_height - size))
        return x, y

    def get_random_spawn_position(self):
        """Get random spawn position within room"""
        import random
        x = random.randint(self.room_x + 50, self.room_x + self.room_width - 150)
        y = random.randint(self.room_y + 50, self.room_y + self.room_height - 150)
        return x, y

    def check_exit_transition(self, player_x, player_y, player_size):
        """Check if player is in exit corridor (after boss killed)"""
        if not self.exit_corridor_open:
            return False

        if not self.door_fully_open:
            return False

        if not self.exit_corridor:
            return False

        corridor = self.exit_corridor

        # Check if player is in the corridor area (horizontally)
        in_corridor_x = corridor['x'] <= player_x <= corridor['x'] + corridor['width']

        if in_corridor_x:
            # Check if player reached the top part of the corridor (allowing some margin)
            # Player should be able to walk through when they reach near the top
            player_top = player_y - player_size/2
            corridor_bottom = corridor['y'] + corridor['height']

            if player_top <= corridor_bottom:
                print(f"🚪 DEBUG: Gracz przechodzi przez złote drzwi! player_y={player_y}, corridor_bottom={corridor_bottom}")
                return True

        return False

    def check_wall_collision(self, player_hitbox, enemies_alive=0, boss_killed=False):
        """Check if player collides with room walls or blocked exit corridor"""
        player_x = player_hitbox.x
        player_y = player_hitbox.y
        player_r = player_hitbox.r

        # Check collision with room boundaries (walls)
        # Left wall
        if player_x - player_r < self.room_x:
            return True
        # Right wall
        if player_x + player_r > self.room_x + self.room_width:
            return True

        # Top wall - special handling for exit corridor
        if player_y - player_r < self.room_y:
            # If boss is killed and exit corridor is open, check if player is in corridor
            if boss_killed and self.exit_corridor_open and self.exit_corridor and self.door_fully_open:
                corridor = self.exit_corridor
                # Allow passage if player is within corridor horizontal bounds
                if corridor['x'] - player_r <= player_x <= corridor['x'] + corridor['width'] + player_r:
                    # Player is in the corridor - allow passage through top wall
                    return False
            # Not in corridor or corridor not open - block top wall
            return True
            # If exit corridor exists, check if player is within corridor bounds
            corridor = self.exit_corridor
            if not (corridor['x'] <= player_x <= corridor['x'] + corridor['width']):
                return True
        # Bottom wall
        if player_y + player_r > self.room_y + self.room_height:
            return True

        return False

