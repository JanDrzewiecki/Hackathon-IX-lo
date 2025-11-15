import pygame
from settings import *
from hit_box import *

class Player:
    def __init__(self, player_start_x, player_start_y):
        self.x = player_start_x
        self.y = player_start_y
        self.hp = 10000000000000
        # self.hp = 60
        self.max_hp = self.hp
        self.ad = 2000000000000
        # self.ad = 20
        self.movement = 5
        self.points = 0

        # Hitbox - use scaled size for proper collision detection
        scaled_width = int(URANEK_FRAME_WIDTH * skale)
        self.hit_box = HitBox(self.x, self.y, scaled_width // 2 - 5, scaled_width // 2)

        # Animation
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 6
        self.frames = self.load_sheet("uranek.png", URANEK_FRAME_WIDTH, URANEK_FRAME_HEIGHT)
        self.current_sprite = self.frames[0]
        self.facing_left = False  # Track if player is facing left

    def load_sheet(self, path, frame_width, frame_height):
        try:
            sheet = pygame.image.load(f"game/{path}").convert_alpha()
        except:
            sheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()

        cols = sheet_width // frame_width
        frames = []

        for col in range(cols):
            rect = pygame.Rect(col * frame_width, 0, frame_width, frame_height)
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), rect)
            frame = pygame.transform.scale(frame, URANEK_SIZE)
            frames.append(frame)

        return frames

    def update(self, keys, room_manager, visited_rooms=None, enemies=None, boss_killed=False):
        # Zapisz poprzednią pozycję
        old_x = self.x
        old_y = self.y

        # Ruch gracza
        moved = False
        if keys[pygame.K_w]:
            self.y -= self.movement
            moved = True
        if keys[pygame.K_s]:
            self.y += self.movement
            moved = True
        if keys[pygame.K_a]:
            self.x -= self.movement
            moved = True
            self.facing_left = True  # Player is moving left (flip sprite)
        if keys[pygame.K_d]:
            self.x += self.movement
            moved = True
            self.facing_left = False  # Player is moving right (normal sprite)

        # Update animation if player is moving
        if moved:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_speed:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.current_sprite = self.frames[self.frame_index]
        else:
            # Reset to first frame when not moving
            self.frame_index = 0
            self.current_sprite = self.frames[0]
            return False

        # Aktualizuj hit_box z nową pozycją
        self.hit_box.update_position(self.x, self.y)

        # Count enemies alive in current room
        enemies_alive = len(enemies) if enemies is not None else 0

        # Sprawdź kolizje ze ścianami (corridors blocked if enemies alive)
        collision = room_manager.check_wall_collision(self.hit_box, enemies_alive)

        if collision:
            # Cofnij ruch przy kolizji
            print(f"COLLISION! Reverting from ({self.x}, {self.y}) to ({old_x}, {old_y})")
            self.x = old_x
            self.y = old_y
            self.hit_box.update_position(old_x, old_y)
            return False

        # Check if player reached the special NEXT LEVEL corridor (boss room) - CHECK THIS FIRST!
        if boss_killed:
            # For FinalRoomManager (level 3), check exit_transition
            if hasattr(room_manager, 'check_exit_transition'):
                if room_manager.check_exit_transition(self.x, self.y, int(URANEK_FRAME_WIDTH * 0.7)):
                    return "next_level"  # Exit after final boss
            # For regular RoomManager (levels 1-2), check special corridor
            elif hasattr(room_manager, 'check_special_corridor'):
                if room_manager.check_special_corridor(self.x, self.y, int(URANEK_FRAME_WIDTH * 0.7)):
                    return "next_level"  # Special return value

        # Sprawdź teleportację do innego pokoju (only for regular RoomManager)
        if hasattr(room_manager, 'check_room_transition'):
            did_teleport = room_manager.check_room_transition(self, enemies_alive)
            return did_teleport

        return False

    def draw(self, screen):
        # Flip sprite horizontally if facing left
        if self.facing_left:
            flipped_sprite = pygame.transform.flip(self.current_sprite, True, False)
            screen.blit(flipped_sprite, (self.x, self.y))
        else:
            screen.blit(self.current_sprite, (self.x, self.y))
