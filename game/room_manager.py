import pygame
import random
from settings import *


class RoomNode:
    """Represents a single room in the game world"""
    def __init__(self, room_id, connections):
        """
        Args:
            room_id: Unique identifier for this room (0-5)
            connections: Dict mapping direction ('top', 'bottom', 'left', 'right') to connected room_id
                        None if no connection in that direction
        """
        self.room_id = room_id
        self.connections = connections  # {'top': room_id or None, 'bottom': ..., 'left': ..., 'right': ...}


class Corridor:
    """Represents a corridor connecting to the edge of the screen"""
    def __init__(self, position, room_x, room_y, room_width, room_height, screen_width, screen_height):
        """
        Args:
            position: 'top', 'bottom', 'left', or 'right'
            room_x, room_y: top-left corner of the room
            room_width, room_height: dimensions of the room
            screen_width, screen_height: screen dimensions
        """
        self.position = position
        self.width = 300  # Width of the corridor (increased to 300px)

        if position == 'top':
            self.x = room_x + room_width // 2 - self.width // 2
            self.y = 0
            self.corridor_width = self.width
            self.corridor_height = room_y
        elif position == 'bottom':
            self.x = room_x + room_width // 2 - self.width // 2
            self.y = room_y + room_height
            self.corridor_width = self.width
            self.corridor_height = screen_height - (room_y + room_height)
        elif position == 'left':
            self.x = 0
            self.y = room_y + room_height // 2 - self.width // 2
            self.corridor_width = room_x
            self.corridor_height = self.width
        elif position == 'right':
            self.x = room_x + room_width
            self.y = room_y + room_height // 2 - self.width // 2
            self.corridor_width = screen_width - (room_x + room_width)
            self.corridor_height = self.width

    def draw(self, screen, room_bg_color):
        """Draw the corridor with same color as room"""
        # Fill corridor with same color as room - no borders
        pygame.draw.rect(screen, room_bg_color,
                        (self.x, self.y, self.corridor_width, self.corridor_height))

    def is_player_in_corridor(self, player_x, player_y, player_size):
        """Check if player is in this corridor"""
        # Check if any part of the player overlaps with the corridor
        return (player_x + player_size > self.x and player_x < self.x + self.corridor_width and
                player_y + player_size > self.y and player_y < self.y + self.corridor_height)

    def reached_edge(self, player_x, player_y, player_size, screen_width, screen_height):
        """Check if player reached the edge of screen through this corridor"""
        if not self.is_player_in_corridor(player_x, player_y, player_size):
            return False

        if self.position == 'top' and player_y <= 0:
            return True
        elif self.position == 'bottom' and player_y + player_size >= screen_height:
            return True
        elif self.position == 'left' and player_x <= 0:
            return True
        elif self.position == 'right' and player_x + player_size >= screen_width:
            return True
        return False


class RoomManager:
    """Manages rooms with corridors and transitions between them"""
    def __init__(self, screen_width, screen_height, margin_pixels=100):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.margin_pixels = margin_pixels

        # Current room dimensions
        self.room_width = screen_width - (2 * margin_pixels)
        self.room_height = screen_height - (2 * margin_pixels)
        self.room_x = margin_pixels
        self.room_y = margin_pixels

        # Room colors
        self.bg_color = (50, 50, 50)
        self.border_color = (255, 255, 255)
        self.border_width = 3

        # Opposite corridors for teleportation (needed by _generate_random_rooms)
        self.opposite = {
            'top': 'bottom',
            'bottom': 'top',
            'left': 'right',
            'right': 'left'
        }

        # Create fixed room layout (same every time)
        # This is a pre-generated layout using seed 42
        self.rooms = self._create_fixed_layout()

        self.current_room_id = 0  # Start in room 0
        self.current_room = self.rooms[self.current_room_id]

        # Build corridors for current room
        self._build_corridors()

    def _create_fixed_layout(self):
        """Create a fixed room layout that never changes"""
        rooms = {}

        # Manually define a fixed layout
        # Layout structure:
        #       [2]
        #        |
        #   [3]-[0]-[1]
        #        |
        #       [4]
        #        |
        #       [5]

        rooms[0] = RoomNode(0, {'top': 2, 'bottom': 4, 'left': 3, 'right': 1})
        rooms[1] = RoomNode(1, {'top': None, 'bottom': None, 'left': 0, 'right': None})
        rooms[2] = RoomNode(2, {'top': None, 'bottom': 0, 'left': None, 'right': None})
        rooms[3] = RoomNode(3, {'top': None, 'bottom': None, 'left': None, 'right': 0})
        rooms[4] = RoomNode(4, {'top': 0, 'bottom': 5, 'left': None, 'right': None})
        rooms[5] = RoomNode(5, {'top': 4, 'bottom': None, 'left': None, 'right': None})

        return rooms


    def _build_corridors(self):
        """Build corridors only for active connections in current room"""
        self.corridors = {}

        for direction, connected_room_id in self.current_room.connections.items():
            if connected_room_id is not None:  # Only create corridor if there's a connection
                self.corridors[direction] = Corridor(
                    direction, self.room_x, self.room_y,
                    self.room_width, self.room_height,
                    self.screen_width, self.screen_height
                )

    def draw(self, screen):
        """Draw the room and only active corridors"""
        # Draw all active corridors first (same color as room, no borders)
        for corridor in self.corridors.values():
            corridor.draw(screen, self.bg_color)

        # Draw main room (same color, seamlessly connects with corridors)
        pygame.draw.rect(screen, self.bg_color,
                        (self.room_x, self.room_y, self.room_width, self.room_height))

        # Draw borders only where there are NO corridors
        border_thickness = self.border_width

        # Top border (with gap if there's a top corridor)
        if 'top' in self.corridors:
            top_corridor = self.corridors['top']
            pygame.draw.line(screen, self.border_color,
                            (self.room_x, self.room_y),
                            (top_corridor.x, self.room_y), border_thickness)
            pygame.draw.line(screen, self.border_color,
                            (top_corridor.x + top_corridor.corridor_width, self.room_y),
                            (self.room_x + self.room_width, self.room_y), border_thickness)
        else:
            # No top corridor, draw full top border
            pygame.draw.line(screen, self.border_color,
                            (self.room_x, self.room_y),
                            (self.room_x + self.room_width, self.room_y), border_thickness)

        # Bottom border (with gap if there's a bottom corridor)
        if 'bottom' in self.corridors:
            bottom_corridor = self.corridors['bottom']
            pygame.draw.line(screen, self.border_color,
                            (self.room_x, self.room_y + self.room_height),
                            (bottom_corridor.x, self.room_y + self.room_height), border_thickness)
            pygame.draw.line(screen, self.border_color,
                            (bottom_corridor.x + bottom_corridor.corridor_width, self.room_y + self.room_height),
                            (self.room_x + self.room_width, self.room_y + self.room_height), border_thickness)
        else:
            # No bottom corridor, draw full bottom border
            pygame.draw.line(screen, self.border_color,
                            (self.room_x, self.room_y + self.room_height),
                            (self.room_x + self.room_width, self.room_y + self.room_height), border_thickness)

        # Left border (with gap if there's a left corridor)
        if 'left' in self.corridors:
            left_corridor = self.corridors['left']
            pygame.draw.line(screen, self.border_color,
                            (self.room_x, self.room_y),
                            (self.room_x, left_corridor.y), border_thickness)
            pygame.draw.line(screen, self.border_color,
                            (self.room_x, left_corridor.y + left_corridor.corridor_height),
                            (self.room_x, self.room_y + self.room_height), border_thickness)
        else:
            # No left corridor, draw full left border
            pygame.draw.line(screen, self.border_color,
                            (self.room_x, self.room_y),
                            (self.room_x, self.room_y + self.room_height), border_thickness)

        # Right border (with gap if there's a right corridor)
        if 'right' in self.corridors:
            right_corridor = self.corridors['right']
            pygame.draw.line(screen, self.border_color,
                            (self.room_x + self.room_width, self.room_y),
                            (self.room_x + self.room_width, right_corridor.y), border_thickness)
            pygame.draw.line(screen, self.border_color,
                            (self.room_x + self.room_width, right_corridor.y + right_corridor.corridor_height),
                            (self.room_x + self.room_width, self.room_y + self.room_height), border_thickness)
        else:
            # No right corridor, draw full right border
            pygame.draw.line(screen, self.border_color,
                            (self.room_x + self.room_width, self.room_y),
                            (self.room_x + self.room_width, self.room_y + self.room_height), border_thickness)

    def check_corridor_transition(self, player_x, player_y, player_size):
        """
        Check if player should transition to a new room
        Returns: (should_transition, new_x, new_y, exit_direction, new_room_id)
        """
        for direction, corridor in self.corridors.items():
            if corridor.reached_edge(player_x, player_y, player_size,
                                    self.screen_width, self.screen_height):
                # Get the room we're transitioning to
                new_room_id = self.current_room.connections[direction]
                if new_room_id is not None:
                    # Calculate spawn position in new room (opposite side)
                    opposite_direction = self.opposite[direction]
                    new_x, new_y = self._get_spawn_position(opposite_direction, player_size)

                    # Switch to new room
                    self.current_room_id = new_room_id
                    self.current_room = self.rooms[new_room_id]
                    self._build_corridors()  # Rebuild corridors for new room

                    return True, new_x, new_y, direction

        return False, None, None, None

    def _get_spawn_position(self, corridor_position, player_size):
        """Get spawn position for player entering from a corridor"""
        offset = 50  # Distance from edge

        # Default values
        x = self.room_x + self.room_width // 2 - player_size // 2
        y = self.room_y + self.room_height // 2 - player_size // 2

        if corridor_position == 'top':
            x = self.room_x + self.room_width // 2 - player_size // 2
            y = self.room_y + offset
        elif corridor_position == 'bottom':
            x = self.room_x + self.room_width // 2 - player_size // 2
            y = self.room_y + self.room_height - player_size - offset
        elif corridor_position == 'left':
            x = self.room_x + offset
            y = self.room_y + self.room_height // 2 - player_size // 2
        elif corridor_position == 'right':
            x = self.room_x + self.room_width - player_size - offset
            y = self.room_y + self.room_height // 2 - player_size // 2

        return x, y

    def is_in_room_or_corridor(self, x, y, object_size):
        """Check if position is valid (in room or corridor)"""
        # Check if in main room
        if (self.room_x <= x and x + object_size <= self.room_x + self.room_width and
            self.room_y <= y and y + object_size <= self.room_y + self.room_height):
            return True

        # Check if in any corridor
        for corridor in self.corridors.values():
            if corridor.is_player_in_corridor(x, y, object_size):
                return True

        return False

    def clamp_position(self, x, y, object_size):
        """Clamp position to keep object inside room or corridors"""
        # Check if player is in main room area (not in corridors)
        in_room = (self.room_x <= x and x + object_size <= self.room_x + self.room_width and
                   self.room_y <= y and y + object_size <= self.room_y + self.room_height)

        if in_room:
            # Player is fully in room, no clamping needed
            return x, y

        # Check each corridor
        for corridor in self.corridors.values():
            if corridor.is_player_in_corridor(x, y, object_size):
                # Player is in a corridor - allow movement to screen edge
                if corridor.position == 'top':
                    # Clamp horizontally to corridor width only
                    x = max(corridor.x, min(x, corridor.x + corridor.corridor_width - object_size))
                    # Allow y to go anywhere (including to 0 and beyond to trigger teleport)
                    return x, y
                elif corridor.position == 'bottom':
                    # Clamp horizontally to corridor width only
                    x = max(corridor.x, min(x, corridor.x + corridor.corridor_width - object_size))
                    # Allow y to go anywhere
                    return x, y
                elif corridor.position == 'left':
                    # Clamp vertically to corridor height only
                    y = max(corridor.y, min(y, corridor.y + corridor.corridor_height - object_size))
                    # Allow x to go anywhere
                    return x, y
                elif corridor.position == 'right':
                    # Clamp vertically to corridor height only
                    y = max(corridor.y, min(y, corridor.y + corridor.corridor_height - object_size))
                    # Allow x to go anywhere
                    return x, y

        # Player is outside room and not in corridor - clamp back to room
        x = max(self.room_x, min(x, self.room_x + self.room_width - object_size))
        y = max(self.room_y, min(y, self.room_y + self.room_height - object_size))
        return x, y

    def get_random_spawn_position(self):
        """Get a random position on one of the room edges for enemy spawning"""
        edge = random.randint(0, 3)

        if edge == 0:  # Top edge
            x = random.randint(self.room_x, self.room_x + self.room_width - ENEMY_SIZE)
            y = self.room_y
        elif edge == 1:  # Bottom edge
            x = random.randint(self.room_x, self.room_x + self.room_width - ENEMY_SIZE)
            y = self.room_y + self.room_height - ENEMY_SIZE
        elif edge == 2:  # Left edge
            x = self.room_x
            y = random.randint(self.room_y, self.room_y + self.room_height - ENEMY_SIZE)
        else:  # Right edge
            x = self.room_x + self.room_width - ENEMY_SIZE
            y = random.randint(self.room_y, self.room_y + self.room_height - ENEMY_SIZE)

        return x, y

    def get_bounds(self):
        """Return the room boundaries (x, y, width, height)"""
        return self.room_x, self.room_y, self.room_width, self.room_height

