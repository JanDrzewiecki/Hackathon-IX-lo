"""
Room Background Manager for handling level-specific backgrounds.
"""
import pygame
import random


class RoomBackgroundManager:
    """
    Manages room backgrounds for different game levels.
    
    Loads and provides random background selection for three levels:
    - Level 1: room-1, room-2, room-3
    - Level 2: room-4, room-5, room-6
    - Level 3: room-7, room-8, room-9
    """
    
    def __init__(self):
        """Initialize background manager and load all backgrounds."""
        self.level1_backgrounds = []  # room-1, room-2, room-3
        self.level2_backgrounds = []  # room-4, room-5, room-6
        self.level3_backgrounds = []  # room-7, room-8, room-9
        self.load_backgrounds()

    def load_backgrounds(self):
        """Load backgrounds for all three levels."""
        # Level 1: room-1, room-2, room-3
        for i in range(1, 4):
            self._load_background(i, self.level1_backgrounds, 1)

        # Level 2: room-4, room-5, room-6
        for i in range(4, 7):
            self._load_background(i, self.level2_backgrounds, 2)

        # Level 3: room-7, room-8, room-9
        for i in range(7, 10):
            self._load_background(i, self.level3_backgrounds, 3)

        print(f"📦 Level 1: {len(self.level1_backgrounds)} backgrounds, "
              f"Level 2: {len(self.level2_backgrounds)} backgrounds, "
              f"Level 3: {len(self.level3_backgrounds)} backgrounds")
    
    def _load_background(self, room_num: int, bg_list: list, level: int):
        """
        Load a single background image.
        
        Args:
            room_num: Room number (1-9)
            bg_list: List to append the loaded background to
            level: Level number for logging
        """
        paths = [f"game/room-{room_num}.png", f"room-{room_num}.png"]
        
        for path in paths:
            try:
                bg = pygame.image.load(path).convert()
                bg_list.append(bg)
                print(f"✓ Loaded room-{room_num}.png (Level {level})")
                return
            except:
                continue
        
        print(f"✗ Cannot load room-{room_num}.png")
    
    def get_random_background(self, level: int = 1):
        """
        Get a random background for the specified level.
        
        Args:
            level: Level number (1, 2, or 3+)
            
        Returns:
            Tuple of (background_surface, room_number) or (None, None) if no backgrounds available
        """
        if level == 1:
            backgrounds = self.level1_backgrounds
            start_idx = 1
        elif level == 2:
            backgrounds = self.level2_backgrounds
            start_idx = 4
        else:  # level 3+
            backgrounds = self.level3_backgrounds
            start_idx = 7

        if backgrounds:
            bg = random.choice(backgrounds)
            idx = backgrounds.index(bg) + start_idx
            return bg, idx
        else:
            return None, None
