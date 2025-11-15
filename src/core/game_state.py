"""
Game state initialization and management.
"""
from src.entities.player import Player
from src.managers.enemy_spawner import EnemySpawner
from src.managers.room_manager import RoomManager
from src.managers.final_room_manager import FinalRoomManager
from src.ui.hud import HeartsHUD
from src.core.constants import URANEK_FRAME_WIDTH, FPS


class GameState:
    """Manages all game state variables."""
    
    def __init__(self, screen_width, screen_height, bg_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_manager = bg_manager
        
        # Core game objects
        self.room_manager = None
        self.player = None
        self.enemies = []
        self.level = 1
        self.enemy_spawner = None
        self.notifications = []
        self.bullets = []
        self.enemy_bullets = []
        self.hud = None
        self.blood_systems = []
        
        # Game progression
        self.visited_rooms = {0}
        self.cleared_rooms = set()
        self.boss_killed = False
        self.current_level = 1
        
        # Cooldowns
        self.bullets_cooldown = 0
        self.damage_cooldown = 0
        
        # Power-up state
        self.shoe_item = None
        self.speed_boost_timer = 0
        self.speed_boost_charges = 0
        self.shield_timer = 0
        self.shield_charges = 0
        self.strength_timer = 0
        self.strength_charges = 0
        self._prev_e_pressed = False
        self._prev_r_pressed = False
        self._prev_t_pressed = False
        self.original_movement = None
        self.original_ad = None
        
        # Drop tracking
        self.current_room_death_counter = 0
        self.current_room_drop_index = None
        self.shoe_dropped_this_level = False
        self.last_powerup_type = None
        
        # Boss bar / intro animation
        self.boss_bar_active = False
        self.boss_bar_target_enemy = None
        self.boss_intro_timer = 0
        self.boss_intro_duration = int(FPS * 1.0)
        self.boss_intro_progress = 0.0
        
        # Room background
        self.room_background = None
    
    def start_new_game(self, keep_current_level=False):
        """
        Reset all game state to start a fresh run.
        
        Args:
            keep_current_level: If True, preserve the current_level value (for level transitions)
        """
        # Store current level if we need to keep it
        saved_level = self.current_level if keep_current_level else 1
        
        # Store power-up charges and type if transitioning between levels
        saved_speed_charges = self.speed_boost_charges if keep_current_level else 0
        saved_shield_charges = self.shield_charges if keep_current_level else 0
        saved_strength_charges = self.strength_charges if keep_current_level else 0
        saved_powerup_type = self.last_powerup_type if keep_current_level else None
        
        # 🎲 Choose random background for the level
        self.room_background, _ = self.bg_manager.get_random_background(level=saved_level)
        
        # Create room manager with corridors
        # For level 4 (after 3 bosses), use FinalRoomManager (single room with final boss)
        if saved_level == 4:
            self.room_manager = FinalRoomManager(self.screen_width, self.screen_height, margin_pixels=100)
        else:
            self.room_manager = RoomManager(self.screen_width, self.screen_height, margin_pixels=100)
        
        # Create player in center of game area
        player_start_x = self.room_manager.room_x + self.room_manager.room_width // 2 - URANEK_FRAME_WIDTH // 2
        player_start_y = self.room_manager.room_y + self.room_manager.room_height // 2 - URANEK_FRAME_WIDTH // 2
        self.player = Player(player_start_x, player_start_y)
        
        # Initialize all game state variables
        self.enemies = []
        self.level = saved_level
        self.enemy_spawner = EnemySpawner(self.level, self.room_manager)
        self.notifications = []
        self.bullets = []
        self.enemy_bullets = []
        self.bullets_cooldown = 0
        self.damage_cooldown = 0
        self.blood_systems = []
        self.visited_rooms = {0}
        self.cleared_rooms = set()
        self.boss_killed = False
        self.current_level = saved_level
        self.hud = HeartsHUD()
        
        # Initialize power-up state
        self.shoe_item = None
        self.speed_boost_timer = 0
        self.speed_boost_charges = saved_speed_charges
        self.shield_timer = 0
        self.shield_charges = saved_shield_charges
        self.strength_timer = 0
        self.strength_charges = saved_strength_charges
        self._prev_e_pressed = False
        self._prev_r_pressed = False
        self._prev_t_pressed = False
        self.original_movement = None
        self.original_ad = None
        
        # Reset boss bar/intro
        self.boss_bar_active = False
        self.boss_bar_target_enemy = None
        self.boss_intro_timer = 0
        self.boss_intro_progress = 0.0
        
        # Reset drop tracking
        self.current_room_death_counter = 0
        self.shoe_dropped_this_level = False
        self.last_powerup_type = saved_powerup_type
        
        # Initialize spawner for first room
        self.enemy_spawner.reset_for_new_room()
        self.current_room_drop_index = None
