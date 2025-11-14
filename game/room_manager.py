import pygame
import random
from settings import *
from hit_box import*
from enemy_type import EnemyType


class RoomNode:
    """Represents a single room with its connections"""
    def __init__(self, room_id):
        self.room_id = room_id
        self.connections = {
            'top': None,
            'bottom': None,
            'left': None,
            'right': None
        }
        # Each room has a random enemy type
        self.enemy_type = random.choice([EnemyType.WEAK, EnemyType.MEDIUM, EnemyType.STRONG])


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
        self.width = 300

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
        pygame.draw.rect(screen, room_bg_color,
                        (self.x, self.y, self.corridor_width, self.corridor_height))

    def is_player_in_corridor(self, player_x, player_y, player_size):
        return (player_x + player_size > self.x and player_x < self.x + self.corridor_width and
                player_y + player_size > self.y and player_y < self.y + self.corridor_height)

    def reached_edge(self, player_x, player_y, player_size, screen_width, screen_height):
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
    """Manages 6 rooms with random connections"""
    def __init__(self, screen_width, screen_height, margin_pixels=100):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.margin_pixels = margin_pixels

        self.room_width = screen_width - (2 * margin_pixels)
        self.room_height = screen_height - (2 * margin_pixels)
        self.room_x = margin_pixels
        self.room_y = margin_pixels

        self.bg_color = (50, 50, 50)
        self.border_color = (255, 255, 255)
        self.border_width = 3

        self.opposite = {
            'top': 'bottom',
            'bottom': 'top',
            'left': 'right',
            'right': 'left'
        }

        # Generate 6 rooms with random connections
        self.rooms = self._generate_6_rooms()

        # Renumber rooms by distance from room 0
        self._renumber_rooms_by_distance()

        self.current_room_id = 0
        self.current_room = self.rooms[0]

        # Initialize walls (will be populated by _build_corridors)
        self.walls = []

        # Print the layout
        self._print_layout()

        # Build corridors for current room (also creates walls)
        self._build_corridors()

    def _generate_6_rooms(self):
        """Generate exactly 6 rooms with random but sensible connections"""
        rooms = {}
        for i in range(6):
            rooms[i] = RoomNode(i)

        # Start with room 0
        connected = {0}
        unconnected = {1, 2, 3, 4, 5}

        directions = ['top', 'bottom', 'left', 'right']

        # Connect all rooms to make a connected graph
        while unconnected:
            # Pick a random room that's already connected
            from_room = random.choice(list(connected))

            # Find available directions
            available = [d for d in directions if rooms[from_room].connections[d] is None]

            if not available:
                continue

            # Pick random direction and room to connect
            direction = random.choice(available)
            to_room = random.choice(list(unconnected))

            # Create bidirectional connection
            rooms[from_room].connections[direction] = to_room
            rooms[to_room].connections[self.opposite[direction]] = from_room

            connected.add(to_room)
            unconnected.remove(to_room)

        return rooms

    def _renumber_rooms_by_distance(self):
        """Renumber rooms based on distance from room 0 (BFS)"""
        # BFS to find distances
        from collections import deque

        # Find distance of each room from room 0
        distances = {}
        queue = deque([(0, 0)])  # (room_id, distance)
        visited = {0}
        distances[0] = 0

        while queue:
            current_id, dist = queue.popleft()

            # Check all connections
            for direction, connected_id in self.rooms[current_id].connections.items():
                if connected_id is not None and connected_id not in visited:
                    visited.add(connected_id)
                    distances[connected_id] = dist + 1
                    queue.append((connected_id, dist + 1))

        # Sort rooms by distance, then by original ID for stability
        sorted_rooms = sorted(distances.keys(), key=lambda x: (distances[x], x))

        # Create mapping from old ID to new ID
        old_to_new = {}
        for new_id, old_id in enumerate(sorted_rooms):
            old_to_new[old_id] = new_id

        # Create new rooms dict with new IDs
        new_rooms = {}
        for old_id, new_id in old_to_new.items():
            new_room = RoomNode(new_id)
            # Update connections with new IDs
            for direction, connected_old_id in self.rooms[old_id].connections.items():
                if connected_old_id is not None:
                    new_room.connections[direction] = old_to_new[connected_old_id]
            new_rooms[new_id] = new_room

        self.rooms = new_rooms

    def _print_layout(self):
        """Print the room layout as a tree with arrows and distances"""
        from collections import deque

        # Calculate distances again for display
        distances = {}
        queue = deque([(0, 0)])
        visited = {0}
        distances[0] = 0

        while queue:
            current_id, dist = queue.popleft()
            for direction, connected_id in self.rooms[current_id].connections.items():
                if connected_id is not None and connected_id not in visited:
                    visited.add(connected_id)
                    distances[connected_id] = dist + 1
                    queue.append((connected_id, dist + 1))

        print("\n" + "="*60)
        print("ROOM LAYOUT - Numbered by distance from Room 0")
        print("="*60)

        for room_id in range(6):
            room = self.rooms[room_id]
            connections = []
            for direction, target in room.connections.items():
                if target is not None:
                    connections.append(f"{direction}→{target}")

            conn_str = ", ".join(connections) if connections else "No connections"
            dist_str = f"(distance: {distances.get(room_id, '?')})"

            # Enemy type info
            enemy_name = room.enemy_type.name
            print(f"  Room [{room_id}] {dist_str} - Enemy: {enemy_name}: {conn_str}")

        print("="*60 + "\n")

    def _build_corridors(self):
        """Build corridors only for current room's connections"""
        self.corridors = {}

        for direction, connected_room in self.current_room.connections.items():
            if connected_room is not None:
                self.corridors[direction] = Corridor(
                    direction, self.room_x, self.room_y,
                    self.room_width, self.room_height,
                    self.screen_width, self.screen_height
                )

        # Create walls after corridors are built
        self.walls = self._create_walls()

    def _create_walls(self):
        """Create wall rectangles for collision detection"""
        walls = []
        thickness = self.border_width

        # Top wall (with gap for top corridor if present)
        if 'top' in self.corridors:
            top_corridor = self.corridors['top']
            # Left section of top wall
            walls.append(pygame.Rect(self.room_x, self.room_y - thickness,
                                     top_corridor.x - self.room_x, thickness))
            # Right section of top wall
            walls.append(pygame.Rect(top_corridor.x + top_corridor.corridor_width, self.room_y - thickness,
                                     self.room_x + self.room_width - (top_corridor.x + top_corridor.corridor_width), thickness))
        else:
            # Full top wall
            walls.append(pygame.Rect(self.room_x, self.room_y - thickness,
                                     self.room_width, thickness))

        # Bottom wall (with gap for bottom corridor if present)
        if 'bottom' in self.corridors:
            bottom_corridor = self.corridors['bottom']
            # Left section of bottom wall
            walls.append(pygame.Rect(self.room_x, self.room_y + self.room_height,
                                     bottom_corridor.x - self.room_x, thickness))
            # Right section of bottom wall
            walls.append(pygame.Rect(bottom_corridor.x + bottom_corridor.corridor_width, self.room_y + self.room_height,
                                     self.room_x + self.room_width - (bottom_corridor.x + bottom_corridor.corridor_width), thickness))
        else:
            # Full bottom wall
            walls.append(pygame.Rect(self.room_x, self.room_y + self.room_height,
                                     self.room_width, thickness))

        # Left wall (with gap for left corridor if present)
        if 'left' in self.corridors:
            left_corridor = self.corridors['left']
            # Top section of left wall
            walls.append(pygame.Rect(self.room_x - thickness, self.room_y,
                                     thickness, left_corridor.y - self.room_y))
            # Bottom section of left wall
            walls.append(pygame.Rect(self.room_x - thickness, left_corridor.y + left_corridor.corridor_height,
                                     thickness, self.room_y + self.room_height - (left_corridor.y + left_corridor.corridor_height)))
        else:
            # Full left wall
            walls.append(pygame.Rect(self.room_x - thickness, self.room_y,
                                     thickness, self.room_height))

        # Right wall (with gap for right corridor if present)
        if 'right' in self.corridors:
            right_corridor = self.corridors['right']
            # Top section of right wall
            walls.append(pygame.Rect(self.room_x + self.room_width, self.room_y,
                                     thickness, right_corridor.y - self.room_y))
            # Bottom section of right wall
            walls.append(pygame.Rect(self.room_x + self.room_width, right_corridor.y + right_corridor.corridor_height,
                                     thickness, self.room_y + self.room_height - (right_corridor.y + right_corridor.corridor_height)))
        else:
            # Full right wall
            walls.append(pygame.Rect(self.room_x + self.room_width, self.room_y,
                                     thickness, self.room_height))

        return walls

    def draw(self, screen):
        """Draw room and active corridors"""
        # Draw corridors
        for corridor in self.corridors.values():
            corridor.draw(screen, self.bg_color)

        # Draw main room
        pygame.draw.rect(screen, self.bg_color,
                        (self.room_x, self.room_y, self.room_width, self.room_height))

        # Draw borders (with gaps for corridors)
        border_thickness = self.border_width

        # Top border
        if 'top' in self.corridors:
            top_corridor = self.corridors['top']
            pygame.draw.line(screen, self.border_color,
                            (self.room_x, self.room_y),
                            (top_corridor.x, self.room_y), border_thickness)
            pygame.draw.line(screen, self.border_color,
                            (top_corridor.x + top_corridor.corridor_width, self.room_y),
                            (self.room_x + self.room_width, self.room_y), border_thickness)
        else:
            pygame.draw.line(screen, self.border_color,
                            (self.room_x, self.room_y),
                            (self.room_x + self.room_width, self.room_y), border_thickness)

        # Bottom border
        if 'bottom' in self.corridors:
            bottom_corridor = self.corridors['bottom']
            pygame.draw.line(screen, self.border_color,
                            (self.room_x, self.room_y + self.room_height),
                            (bottom_corridor.x, self.room_y + self.room_height), border_thickness)
            pygame.draw.line(screen, self.border_color,
                            (bottom_corridor.x + bottom_corridor.corridor_width, self.room_y + self.room_height),
                            (self.room_x + self.room_width, self.room_y + self.room_height), border_thickness)
        else:
            pygame.draw.line(screen, self.border_color,
                            (self.room_x, self.room_y + self.room_height),
                            (self.room_x + self.room_width, self.room_y + self.room_height), border_thickness)

        # Left border
        if 'left' in self.corridors:
            left_corridor = self.corridors['left']
            pygame.draw.line(screen, self.border_color,
                            (self.room_x, self.room_y),
                            (self.room_x, left_corridor.y), border_thickness)
            pygame.draw.line(screen, self.border_color,
                            (self.room_x, left_corridor.y + left_corridor.corridor_height),
                            (self.room_x, self.room_y + self.room_height), border_thickness)
        else:
            pygame.draw.line(screen, self.border_color,
                            (self.room_x, self.room_y),
                            (self.room_x, self.room_y + self.room_height), border_thickness)

        # Right border
        if 'right' in self.corridors:
            right_corridor = self.corridors['right']
            pygame.draw.line(screen, self.border_color,
                            (self.room_x + self.room_width, self.room_y),
                            (self.room_x + self.room_width, right_corridor.y), border_thickness)
            pygame.draw.line(screen, self.border_color,
                            (self.room_x + self.room_width, right_corridor.y + right_corridor.corridor_height),
                            (self.room_x + self.room_width, self.room_y + self.room_height), border_thickness)
        else:
            pygame.draw.line(screen, self.border_color,
                            (self.room_x + self.room_width, self.room_y),
                            (self.room_x + self.room_width, self.room_y + self.room_height), border_thickness)

    def check_corridor_transition(self, player_x, player_y, player_size):
        """Check if player should move to another room"""
        for direction, corridor in self.corridors.items():
            if corridor.reached_edge(player_x, player_y, player_size,
                                    self.screen_width, self.screen_height):
                new_room_id = self.current_room.connections[direction]
                if new_room_id is not None:
                    opposite_direction = self.opposite[direction]
                    new_x, new_y = self._get_spawn_position(opposite_direction, player_size)

                    # Switch to new room
                    self.current_room_id = new_room_id
                    self.current_room = self.rooms[new_room_id]
                    self._build_corridors()

                    return True, new_x, new_y, direction

        return False, None, None, None

    def _get_spawn_position(self, corridor_position, player_size):
        """Get spawn position when entering from a corridor"""
        offset = 50
        x = self.room_x + self.room_width // 2 - player_size // 2
        y = self.room_y + self.room_height // 2 - player_size // 2

        if corridor_position == 'top':
            y = self.room_y + offset
        elif corridor_position == 'bottom':
            y = self.room_y + self.room_height - player_size - offset
        elif corridor_position == 'left':
            x = self.room_x + offset
        elif corridor_position == 'right':
            x = self.room_x + self.room_width - player_size - offset

        return x, y

    def clamp_position(self, x, y, object_size):
        """Clamp position to room or corridors"""
        in_room = (self.room_x <= x and x + object_size <= self.room_x + self.room_width and
                   self.room_y <= y and y + object_size <= self.room_y + self.room_height)

        if in_room:
            return x, y

        for corridor in self.corridors.values():
            if corridor.is_player_in_corridor(x, y, object_size):
                if corridor.position == 'top':
                    x = max(corridor.x, min(x, corridor.x + corridor.corridor_width - object_size))
                    return x, y
                elif corridor.position == 'bottom':
                    x = max(corridor.x, min(x, corridor.x + corridor.corridor_width - object_size))
                    return x, y
                elif corridor.position == 'left':
                    y = max(corridor.y, min(y, corridor.y + corridor.corridor_height - object_size))
                    return x, y
                elif corridor.position == 'right':
                    y = max(corridor.y, min(y, corridor.y + corridor.corridor_height - object_size))
                    return x, y

        x = max(self.room_x, min(x, self.room_x + self.room_width - object_size))
        y = max(self.room_y, min(y, self.room_y + self.room_height - object_size))
        return x, y

    def get_random_spawn_position(self):
        """Get random position on room edge for enemy spawning"""
        edge = random.randint(0, 3)
        if edge == 0:
            x = random.randint(self.room_x, self.room_x + self.room_width - ENEMY_SIZE)
            y = self.room_y
        elif edge == 1:
            x = random.randint(self.room_x, self.room_x + self.room_width - ENEMY_SIZE)
            y = self.room_y + self.room_height - ENEMY_SIZE
        elif edge == 2:
            x = self.room_x
            y = random.randint(self.room_y, self.room_y + self.room_height - ENEMY_SIZE)
        else:
            x = self.room_x + self.room_width - ENEMY_SIZE
            y = random.randint(self.room_y, self.room_y + self.room_height - ENEMY_SIZE)
        return x, y

    def get_bounds(self):
        """Return room boundaries"""
        return self.room_x, self.room_y, self.room_width, self.room_height

    def check_wall_collision(self, player_hitbox):
        """Check if player (circular hitbox) collides with any wall (rectangle)"""
        for wall in self.walls:
            # Check circle-to-rectangle collision
            # Find the closest point on the rectangle to the circle center
            closest_x = max(wall.x, min(player_hitbox.x, wall.x + wall.width))
            closest_y = max(wall.y, min(player_hitbox.y, wall.y + wall.height))

            # Calculate distance from circle center to this closest point
            distance_x = player_hitbox.x - closest_x
            distance_y = player_hitbox.y - closest_y

            # If the distance is less than the circle's radius, there's a collision
            distance_squared = distance_x * distance_x + distance_y * distance_y
            if distance_squared < (player_hitbox.r * player_hitbox.r):
                return True
        return False

    def check_room_transition(self, player):
        """Check if player should transition to a new room and update position"""
        # Get player size - using the scaled URANEK size
        player_size = int(URANEK_FRAME_WIDTH * 0.7)  # matching the scale from settings

        should_transition, new_x, new_y, direction = self.check_corridor_transition(
            player.x, player.y, player_size
        )

        if should_transition:
            player.x = new_x
            player.y = new_y
            player.hit_box.x = new_x
            player.hit_box.y = new_y
            return True

        return False

