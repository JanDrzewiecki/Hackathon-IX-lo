import pygame
from settings import *
from hit_box import *
from enemy_type import EnemyType, EnemyTypeConfig
from hud import load_heart_images


class Enemy:
    # Cached heart images for all enemies to avoid reloading each frame
    _heart_img = None
    _dim_heart_img = None

    def __init__(self, x, y, enemy_type=EnemyType.WEAK, room=None, level=1):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.level = level  # Store level for boss sprite selection

        # Get stats from enemy type config
        config = EnemyTypeConfig.get_config(enemy_type)
        self.hp = config['hp']
        self.max_hp = config['hp']
        self.ad = config['ad']
        self.movement = config['speed']
        self.color = config['color']
        self.size = config['size']

        self.hit_box = HitBox(self.x, self.y, self.size // 2 - 2, self.size // 2)
        self.room = room

        # Animation properties
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 8  # Animation speed
        self.frames = []
        self.current_sprite = None
        self.facing_left = False  # Track if enemy is facing left

        # Load sprite sheet based on enemy type and level
        if self.enemy_type == EnemyType.WEAK:
            if level == 2:
                self.frames = self.load_sheet("enemy4.png", 100, 100)
            elif level == 3:
                self.frames = self.load_sheet("enemy7.png", 100, 100)
            else:  # level 1
                self.frames = self.load_sheet("enemy1.png", 100, 100)
            if self.frames:
                self.current_sprite = self.frames[0]
        elif self.enemy_type == EnemyType.MEDIUM:
            if level == 2:
                self.frames = self.load_sheet("enemy5.png", 100, 100)
            elif level == 3:
                self.frames = self.load_sheet("enemy8.png", 100, 100)
            else:  # level 1
                self.frames = self.load_sheet("enemy2.png", 100, 100)
            if self.frames:
                self.current_sprite = self.frames[0]
        elif self.enemy_type == EnemyType.STRONG:
            if level == 2:
                self.frames = self.load_sheet("enemy6.png", 100, 100)
            elif level == 3:
                self.frames = self.load_sheet("enemy9.png", 100, 100)
            else:  # level 1
                self.frames = self.load_sheet("enemy3.png", 100, 100)
            if self.frames:
                self.current_sprite = self.frames[0]
        elif self.enemy_type == EnemyType.BOSS:
            # Use different boss sprite based on level
            if level == 2:
                # Level 2: Trash Boss (100x200)
                self.frames = self.load_sheet("trash-boss.png", 100, 200)
            elif level == 3:
                # Level 3: Olejman Boss (400x200 = 4 frames of 100x200)
                self.frames = self.load_sheet("olejman-boss.png", 100, 200)
            else:
                # Level 1 (and others): Coal Boss (200x200)
                self.frames = self.load_sheet("coal-boss.png", 200, 200)
            if self.frames:
                self.current_sprite = self.frames[0]
        elif self.enemy_type == EnemyType.FINAL_BOSS:
            # Final Boss sprite sheet is 800x200 - 4 frames of 200x200
            self.frames = self.load_sheet("final-boss.png", 200, 200)
            if self.frames:
                self.current_sprite = self.frames[0]

        # Boss shooting mechanics
        self.is_boss = (enemy_type == EnemyType.BOSS or enemy_type == EnemyType.FINAL_BOSS)
        if self.is_boss:
            self.shoot_cooldown = 0
            # Olejman Boss (level 3) has longer cooldown: 2 seconds (120 frames at 60 FPS)
            if level == 3:
                self.shoot_cooldown_max = FPS * 2  # 2 seconds for Olejman Boss
            else:
                self.shoot_cooldown_max = config.get('shoot_cooldown', 120)
            # Burst fire mechanics
            self.burst_count = 0  # Current bullet in burst (0-2)
            self.burst_delay = 12  # Frames between shots in burst (12 frames = 0.20s at 60 FPS)
            self.burst_delay_counter = 0
            # Fire sprite cycling for trash boss (level 2)
            self.fire_sprite_index = 0  # Cycles between 0, 1, 2 for trash-boss-fire1/2/3

            # Final boss (level 4) - Cycle shooting mechanics
            if enemy_type == EnemyType.FINAL_BOSS:
                self.firing_phase_duration = FPS * 5  # 5 seconds of shooting (300 frames at 60 FPS)
                self.cooldown_phase_duration = FPS * 2  # 2 seconds of cooldown (120 frames at 60 FPS)
                self.phase_timer = 0  # Current timer in phase
                self.is_firing_phase = True  # Start in firing phase

        # Prepare heart icons once (shared)
        self._ensure_hearts_loaded()

    def _ensure_hearts_loaded(self):
        if Enemy._heart_img is None or Enemy._dim_heart_img is None:
            heart, dim = load_heart_images(16, './heart2.png')
            Enemy._heart_img = heart
            Enemy._dim_heart_img = dim

    def load_sheet(self, path, frame_width, frame_height):
        """Load sprite sheet and split it into individual frames"""
        try:
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
                frames.append(frame)

            return frames
        except Exception as e:
            print(f"Error loading enemy sprite {path}: {e}")
            return []

    def set_room(self, room):
        """Set the room boundaries for this enemy."""
        self.room = room

    def _draw_enemy_hearts(self, screen):
        # Each heart represents 10 HP (as per example: 50 HP -> 5 hearts)
        hp_per_heart = 10
        total_hearts = max(1, int((self.max_hp + hp_per_heart - 1) // hp_per_heart))

        # Visual size of hearts relative to enemy size
        heart_size = max(10, min(20, int(self.size * 0.4)))
        spacing = 2
        # If we just loaded default size 16 previously, but heart_size differs, rescale once
        if Enemy._heart_img is not None and Enemy._heart_img.get_width() != heart_size:
            try:
                Enemy._heart_img = pygame.transform.smoothscale(Enemy._heart_img, (heart_size, heart_size))
                Enemy._dim_heart_img = pygame.transform.smoothscale(Enemy._dim_heart_img, (heart_size, heart_size))
            except Exception:
                pass

        total_width = total_hearts * heart_size + (total_hearts - 1) * spacing
        x0 = self.x + (self.size - total_width) // 2

        # For bosses we don't draw the bar here; main will render a centralized animated boss bar.
        if self.is_boss:
            return

        extra_offset = 0
        y0 = self.y - heart_size - 4 - extra_offset

        # Compute how many hearts are fully/partially filled based on current HP in units of 10
        shown_hp = max(0, min(self.hp, self.max_hp))
        hearts_value = shown_hp / float(hp_per_heart)

        use_fallback = (Enemy._heart_img is None or Enemy._dim_heart_img is None)

        for i in range(total_hearts):
            x = x0 + i * (heart_size + spacing)
            filled = hearts_value - i  # 1.0 = full, 0.0 = empty, in-between = partial
            if filled <= 0:
                if use_fallback:
                    # Draw dim rect
                    s = pygame.Surface((heart_size, heart_size), pygame.SRCALPHA)
                    pygame.draw.rect(s, (80, 80, 80, 140), s.get_rect(), border_radius=heart_size // 4)
                    screen.blit(s, (x, y0))
                else:
                    screen.blit(Enemy._dim_heart_img, (x, y0))
                continue
            if use_fallback:
                # Draw dim background then filled portion as red rect
                s = pygame.Surface((heart_size, heart_size), pygame.SRCALPHA)
                pygame.draw.rect(s, (80, 80, 80, 140), s.get_rect(), border_radius=heart_size // 4)
                screen.blit(s, (x, y0))
                w = heart_size if filled >= 1 else max(1, int(filled * heart_size))
                fg = pygame.Surface((w, heart_size), pygame.SRCALPHA)
                pygame.draw.rect(fg, (220, 30, 30, 255), fg.get_rect(), border_radius=heart_size // 4)
                screen.blit(fg, (x, y0))
            else:
                if filled >= 1:
                    screen.blit(Enemy._heart_img, (x, y0))
                else:
                    # Draw dim then overlay clipped heart for partial fill
                    screen.blit(Enemy._dim_heart_img, (x, y0))
                    w = max(1, int(filled * heart_size))
                    area = pygame.Rect(0, 0, w, heart_size)
                    screen.blit(Enemy._heart_img, (x, y0), area=area)

    def draw(self, screen):
        # Draw animated sprite for all enemy types with sprites
        if self.current_sprite:
            # Flip sprite horizontally if facing left
            if self.facing_left:
                flipped_sprite = pygame.transform.flip(self.current_sprite, True, False)
                sprite_rect = flipped_sprite.get_rect(center=(int(self.x + self.size // 2), int(self.y + self.size // 2)))
                screen.blit(flipped_sprite, sprite_rect)
            else:
                sprite_rect = self.current_sprite.get_rect(center=(int(self.x + self.size // 2), int(self.y + self.size // 2)))
                screen.blit(self.current_sprite, sprite_rect)
        else:
            # Fallback: Draw colored square if no sprite loaded
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))


        # Draw hearts above enemy
        self._draw_enemy_hearts(screen)

    def update(self, player_x, player_y, enemy_bullets=None):
        # Update animation for all enemies with frames
        if self.frames:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_speed:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.current_sprite = self.frames[self.frame_index]

        # calculating direction to the player
        vx = self.x - player_x
        vy = self.y - player_y
        normalize_factor = (vx ** 2 + vy ** 2) ** 0.5

        # Avoid division by zero when enemy is at same position as player
        if normalize_factor == 0:
            return

        vx /= normalize_factor
        vy /= normalize_factor

        # Track facing direction based on horizontal movement
        # vx > 0 means enemy is to the right of player, so moving left (towards player) - face right
        # vx < 0 means enemy is to the left of player, so moving right (towards player) - face left
        # Special case: enemy8 (eye) faces opposite direction
        is_enemy8 = (self.level == 3 and self.enemy_type == EnemyType.MEDIUM)
        if vx > 0:
            self.facing_left = True if is_enemy8 else False  # Enemy is right of player, moving left
        elif vx < 0:
            self.facing_left = False if is_enemy8 else True  # Enemy is left of player, moving right

        # updating position
        new_x = self.x - vx * self.movement
        new_y = self.y - vy * self.movement

        # Clamp position to room boundaries if room is set
        if self.room:
            new_x, new_y = self.room.clamp_position(new_x, new_y, self.size)

        # Store old position for collision detection
        old_x = self.x
        old_y = self.y

        # Temporarily update position and hitbox to check collisions
        self.x = new_x
        self.y = new_y
        self.hit_box.update_position(self.x, self.y)

        # Check collision with other enemies - revert if collision detected
        # This will be called from main.py with the enemies list

        # Position is updated here, but may be reverted in check_enemy_collisions if needed

        # Boss shooting - burst fire (3 bullets in quick succession) for regular bosses
        # Full auto (continuous single shots) for final boss
        if self.is_boss and enemy_bullets is not None:
            # Main cooldown between shots
            self.shoot_cooldown -= 1

            # FINAL BOSS - Full auto with cycling phases (5s shooting, 2s cooldown)
            if self.level == 4:
                # Update phase timer
                self.phase_timer += 1

                if self.is_firing_phase:
                    # FIRING PHASE (5 seconds)
                    if self.phase_timer >= self.firing_phase_duration:
                        # Switch to cooldown phase
                        self.is_firing_phase = False
                        self.phase_timer = 0
                    else:
                        # Fire full auto during firing phase
                        if self.shoot_cooldown <= 0:
                            from enemy_bullet import EnemyBullet

                            boss_center_x = self.x + self.size // 2
                            boss_center_y = self.y + self.size // 2

                            # Fire single bullet directly at player (full auto)
                            bullet = EnemyBullet(boss_center_x, boss_center_y, player_x, player_y,
                                               level=self.level, fire_sprite_index=0)
                            enemy_bullets.append(bullet)

                            # Reset cooldown for next shot (very fast for full auto)
                            self.shoot_cooldown = self.shoot_cooldown_max
                else:
                    # COOLDOWN PHASE (2 seconds) - no shooting
                    if self.phase_timer >= self.cooldown_phase_duration:
                        # Switch back to firing phase
                        self.is_firing_phase = True
                        self.phase_timer = 0
            else:
                # REGULAR BOSSES - Burst fire or single shot logic
                # Olejman Boss (level 3) - Single shot with cooldown (no burst)
                if self.level == 3:
                    if self.shoot_cooldown <= 0:
                        from enemy_bullet import EnemyBullet

                        boss_center_x = self.x + self.size // 2
                        boss_center_y = self.y + self.size // 2

                        # OLEJMAN BOSS - Fire single huge bullet directly at player
                        bullet = EnemyBullet(boss_center_x, boss_center_y, player_x, player_y,
                                           level=self.level, fire_sprite_index=0)
                        enemy_bullets.append(bullet)

                        # Reset cooldown (2 seconds)
                        self.shoot_cooldown = self.shoot_cooldown_max
                else:
                    # OTHER BOSSES - Burst fire logic (3 bullets in quick succession)
                    if self.shoot_cooldown <= 0 and self.burst_count < 3:
                        self.burst_delay_counter -= 1

                        if self.burst_delay_counter <= 0:
                            from enemy_bullet import EnemyBullet
                            import math

                            boss_center_x = self.x + self.size // 2
                            boss_center_y = self.y + self.size // 2

                            if self.level == 2:
                                # TRASH BOSS - Fire in 8 directions (every 45 degrees), one bullet per direction
                                num_directions = 8
                                for i in range(num_directions):
                                    direction_angle = math.radians(i * 45)  # Convert to radians

                                    distance = 500
                                    target_x = boss_center_x + math.cos(direction_angle) * distance
                                    target_y = boss_center_y + math.sin(direction_angle) * distance

                                    # Pass level and fire_sprite_index to bullet
                                    bullet = EnemyBullet(boss_center_x, boss_center_y, target_x, target_y,
                                                       level=self.level, fire_sprite_index=self.fire_sprite_index)
                                    enemy_bullets.append(bullet)

                                # Cycle fire sprite for trash boss (0 -> 1 -> 2 -> 0)
                                self.fire_sprite_index = (self.fire_sprite_index + 1) % 3
                            else:
                                # COAL BOSS (level 1) - Fire shotgun spread (3 bullets) towards player
                                dx = player_x - boss_center_x
                                dy = player_y - boss_center_y
                                base_angle = math.atan2(dy, dx)

                                # Shotgun spread: 3 bullets with 37 degree spread
                                spread_angle = math.radians(37)  # 37 degrees to each side
                                angles = [
                                    base_angle - spread_angle,  # Left
                                    base_angle,                  # Center
                                    base_angle + spread_angle    # Right
                                ]

                                for angle in angles:
                                    distance = 500
                                    target_x = boss_center_x + math.cos(angle) * distance
                                    target_y = boss_center_y + math.sin(angle) * distance

                                    bullet = EnemyBullet(boss_center_x, boss_center_y, target_x, target_y,
                                                       level=self.level, fire_sprite_index=0)
                                    enemy_bullets.append(bullet)

                            self.burst_count += 1
                            self.burst_delay_counter = self.burst_delay

                            # If burst is complete, reset cooldown
                            if self.burst_count >= 3:
                                self.shoot_cooldown = self.shoot_cooldown_max
                                self.burst_count = 0
                            self.shoot_cooldown = self.shoot_cooldown_max
                            self.burst_count = 0

    def check_collision_with_enemies(self, other_enemies):
        """Check if this enemy collides with any other enemy and revert position if needed.

        Args:
            other_enemies: List of all enemies (including self)
        """
        for other in other_enemies:
            # Skip self
            if other is self:
                continue

            # Check if hitboxes collide
            if self.hit_box.collide(other.hit_box):
                # Collision detected! Push enemies apart
                # Calculate vector from other enemy to this enemy
                dx = self.x - other.x
                dy = self.y - other.y
                distance = (dx**2 + dy**2)**0.5

                if distance == 0:
                    # Enemies are at exact same position, push randomly
                    import random
                    dx = random.choice([-1, 1])
                    dy = random.choice([-1, 1])
                    distance = 1.414  # sqrt(2)

                # Normalize
                dx /= distance
                dy /= distance

                # Push apart by minimum separation distance
                min_separation = (self.size + other.size) // 2
                overlap = min_separation - distance

                if overlap > 0:
                    # Push this enemy away from other enemy
                    push_distance = (overlap / 2) + 1  # Split the push
                    self.x += dx * push_distance
                    self.y += dy * push_distance

                    # Clamp to room boundaries
                    if self.room:
                        self.x, self.y = self.room.clamp_position(self.x, self.y, self.size)

                    # Update hitbox
                    self.hit_box.update_position(self.x, self.y)

                # Only handle one collision per frame to avoid jittering
                return True

        return False
