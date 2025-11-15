import os
import pygame


def load_heart_images(heart_height: int, image_path: str = './heart2.png'):
    try:
        img = pygame.image.load(image_path).convert_alpha()
    except Exception:
        try:
            alt = os.path.join(os.path.dirname(__file__), os.path.basename(image_path))
            img = pygame.image.load(alt).convert_alpha()
        except Exception:
            return None, None
    raw_w, raw_h = img.get_size()
    if raw_h <= 0:
        return None, None
    scale = heart_height / raw_h
    new_w = max(1, int(raw_w * scale))
    new_h = max(1, int(raw_h * scale))
    heart = pygame.transform.smoothscale(img, (new_w, new_h))
    dim = heart.copy()
    shade = pygame.Surface((new_w, new_h), pygame.SRCALPHA)
    shade.fill((160, 160, 160, 255))
    dim.blit(shade, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    dim.set_alpha(140)
    return heart, dim


def _ease_out_back(t: float) -> float:
    # nice popping easing for animations
    c1 = 1.70158
    c3 = c1 + 1
    t = max(0.0, min(1.0, t))
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


class HeartsHUD:
    def __init__(self, hp_per_heart: int = 20, heart_size: int = 72, spacing: int = 1,
                 pos=(10, 10), image_path: str = './heart2.png'):
        self.hp_per_heart = hp_per_heart
        self.heart_size = heart_size
        self.spacing = spacing
        self.x0, self.y0 = pos

        self.heart, self.dim_heart = load_heart_images(heart_size, image_path)

        # Animations state
        self.prev_hp = None
        # per-slot: {'start': ms, 'duration': ms, 'power': float}
        self.anim = {}

        # Shoe boost HUD assets (lazy-init on first draw)
        self._shoe_icon = None
        self._shoe_size = int(self.heart_size * 0.85)
        self._font_small = None
        # Shield HUD assets
        self._shield_icon = None
        self._shield_size = int(self.heart_size * 0.85)

    def _trigger_loss_anim(self, slot_idx: int, half_steps_lost: int):
        # stronger animation for full-heart loss (2 half-steps)
        power = 1.0 if half_steps_lost >= 2 else 0.55
        duration = 420 if half_steps_lost >= 2 else 260
        now = pygame.time.get_ticks()
        self.anim[slot_idx] = {'start': now, 'duration': duration, 'power': power}

    def _get_anim_scale(self, slot_idx: int):
        a = self.anim.get(slot_idx)
        if not a:
            return 1.0
        now = pygame.time.get_ticks()
        t = (now - a['start']) / max(1, a['duration'])
        if t >= 1.0:
            # end animation
            self.anim.pop(slot_idx, None)
            return 1.0
        # simple popping scale
        pop = _ease_out_back(t) * 0.25 * a['power']
        scale = 1.0 + pop
        return scale

    def _ensure_shoe_assets(self):
        if self._shoe_icon is None:
            img = None
            try:
                img = pygame.image.load("game/boost_shoe2.png").convert_alpha()
            except Exception:
                try:
                    img = pygame.image.load("boost_shoe2.png").convert_alpha()
                except Exception:
                    img = None
            if img is None:
                surf = pygame.Surface((self._shoe_size, self._shoe_size), pygame.SRCALPHA)
                surf.fill((220, 60, 60))
                self._shoe_icon = surf
            else:
                self._shoe_icon = pygame.transform.smoothscale(img, (self._shoe_size, self._shoe_size))
        if self._font_small is None:
            # Use default font scaled to shoe size
            size = max(12, int(self._shoe_size * 0.9))
            self._font_small = pygame.font.Font(None, size)

    def _ensure_shield_assets(self):
        if self._shield_icon is None:
            img = None
            paths = (
                "game/shield.png",
                "shield.png",
                "game/shield.jpg.avif",
                "shield.jpg.avif",
                "game/boost_shield.png",
                "boost_shield.png",
            )
            # Try pygame loader first
            for path in paths:
                try:
                    img = pygame.image.load(path).convert_alpha()
                    break
                except Exception:
                    img = None
            # If AVIF not supported by pygame, try optional PIL fallback
            if img is None:
                try:
                    from PIL import Image
                    import os
                    for path in paths:
                        if os.path.exists(path) and path.lower().endswith(".avif"):
                            pil_img = Image.open(path).convert("RGBA")
                            mode = pil_img.mode
                            size = pil_img.size
                            data = pil_img.tobytes()
                            img = pygame.image.fromstring(data, size, mode).convert_alpha()
                            break
                except Exception:
                    img = None
            if img is None:
                # Blue circle fallback
                size = self._shield_size
                surf = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.circle(surf, (80, 160, 255), (size//2, size//2), size//2)
                pygame.draw.circle(surf, (200, 230, 255), (size//2, size//2), size//2, 3)
                self._shield_icon = surf
            else:
                self._shield_icon = pygame.transform.smoothscale(img, (self._shield_size, self._shield_size))
        # Ensure small font exists even if only shield is present (fix crash)
        if self._font_small is None:
            size = max(12, int(self._shield_size * 0.9))
            self._font_small = pygame.font.Font(None, size)

    def draw(self, surface: pygame.Surface, player_obj, speed_boost_seconds=None, speed_boost_charges=None, shield_seconds=None, shield_charges=None):
        slots = min(3, max(1, player_obj.max_hp // self.hp_per_heart))
        max_shown = slots * self.hp_per_heart
        shown_hp = max(0, min(player_obj.hp, max_shown))

        # Detect losses (heart or half-heart) per slot
        if self.prev_hp is None:
            self.prev_hp = shown_hp
        prev_shown = max(0, min(self.prev_hp, max_shown))

        # compare quantized to halves in each slot
        for i in range(slots):
            prev_filled = (prev_shown - i * self.hp_per_heart) / self.hp_per_heart
            curr_filled = (shown_hp - i * self.hp_per_heart) / self.hp_per_heart
            q_prev = max(0, min(2, int(prev_filled * 2 + 1e-6)))
            q_curr = max(0, min(2, int(curr_filled * 2 + 1e-6)))
            if q_curr < q_prev:
                self._trigger_loss_anim(i, q_prev - q_curr)

        self.prev_hp = shown_hp

        have_img = (self.heart is not None and self.dim_heart is not None)
        heart_w = self.heart.get_width() if have_img else self.heart_size
        heart_h = self.heart.get_height() if have_img else self.heart_size
        step_w = heart_w + self.spacing

        for i in range(slots):
            base_x = self.x0 + i * step_w
            y = self.y0
            filled = (shown_hp - i * self.hp_per_heart) / self.hp_per_heart

            # compute animation scale only (no shake for simplicity)
            scale = self._get_anim_scale(i)

            if filled <= 0:
                # empty slot
                if have_img:
                    img = self.dim_heart
                    if scale != 1.0:
                        # scale around center
                        w2 = max(1, int(heart_w * scale))
                        h2 = max(1, int(heart_h * scale))
                        scaled = pygame.transform.smoothscale(img, (w2, h2))
                        x = base_x + (heart_w - w2) // 2
                        surface.blit(scaled, (x, y + (heart_h - h2) // 2))
                    else:
                        surface.blit(img, (base_x, y))
                else:
                    bg = pygame.Surface((heart_w, heart_h), pygame.SRCALPHA)
                    pygame.draw.rect(bg, (80, 80, 80, 140), bg.get_rect(), border_radius=heart_h // 4)
                    if scale != 1.0:
                        w2 = max(1, int(heart_w * scale))
                        h2 = max(1, int(heart_h * scale))
                        bg = pygame.transform.smoothscale(bg, (w2, h2))
                        x = base_x + (heart_w - w2) // 2
                        surface.blit(bg, (x, y + (heart_h - h2) // 2))
                    else:
                        surface.blit(bg, (base_x, y))
                continue

            # draw background dim then filled portion, with animation scaling
            draw_x = base_x
            if have_img:
                # compose into a temporary surface to scale together
                temp = pygame.Surface((heart_w, heart_h), pygame.SRCALPHA)
                if filled >= 1:
                    temp.blit(self.heart, (0, 0))
                else:
                    temp.blit(self.dim_heart, (0, 0))
                    w = max(1, int(filled * heart_w))
                    area = pygame.Rect(0, 0, w, heart_h)
                    temp.blit(self.heart, (0, 0), area=area)
                if scale != 1.0:
                    w2 = max(1, int(heart_w * scale))
                    h2 = max(1, int(heart_h * scale))
                    temp = pygame.transform.smoothscale(temp, (w2, h2))
                    draw_x = base_x + (heart_w - w2) // 2
                    surface.blit(temp, (draw_x, y + (heart_h - h2) // 2))
                else:
                    surface.blit(temp, (draw_x, y))
            else:
                bg = pygame.Surface((heart_w, heart_h), pygame.SRCALPHA)
                pygame.draw.rect(bg, (80, 80, 80, 140), bg.get_rect(), border_radius=heart_h // 4)
                w = max(1, int(min(1.0, filled) * heart_w))
                fg = pygame.Surface((w, heart_h), pygame.SRCALPHA)
                pygame.draw.rect(fg, (220, 30, 30, 255), fg.get_rect(), border_radius=heart_h // 4)
                temp = pygame.Surface((heart_w, heart_h), pygame.SRCALPHA)
                temp.blit(bg, (0, 0))
                temp.blit(fg, (0, 0))
                if scale != 1.0:
                    w2 = max(1, int(heart_w * scale))
                    h2 = max(1, int(heart_h * scale))
                    temp = pygame.transform.smoothscale(temp, (w2, h2))
                    draw_x = base_x + (heart_w - w2) // 2
                    surface.blit(temp, (draw_x, y + (heart_h - h2) // 2))
                else:
                    surface.blit(temp, (draw_x, y))

        # Draw shoe speed boost icon, charges and countdown to the right of hearts
        shoe_active = (speed_boost_seconds is not None and speed_boost_seconds > 0)
        shoe_have = (speed_boost_charges is not None and speed_boost_charges > 0)
        draw_x = self.x0 + slots * step_w + self.spacing * 4
        if shoe_active or shoe_have:
            self._ensure_shoe_assets()
            y = self.y0 + max(0, (heart_h - self._shoe_size) // 2)
            # Icon
            surface.blit(self._shoe_icon, (draw_x, y))
            # Charges text (e.g., x3) with activation key hint
            charges_txt = f"x{max(0, int(speed_boost_charges or 0))} (E)"
            charges_surf = self._font_small.render(charges_txt, True, (255, 255, 255))
            cx = draw_x + self._shoe_size + 10
            cy = y + (self._shoe_size - charges_surf.get_height()) // 2
            surface.blit(charges_surf, (cx, cy))
            end_x = cx + charges_surf.get_width()
            # If active, show countdown after charges (transparent background)
            if shoe_active:
                secs = int(max(0, speed_boost_seconds))
                text_surf = self._font_small.render(str(secs), True, (255, 255, 255))
                box_x = end_x + 10
                box_y = y + (self._shoe_size - text_surf.get_height()) // 2
                surface.blit(text_surf, (box_x, box_y))
                end_x = box_x + text_surf.get_width()
            draw_x = (end_x + 20) if 'end_x' in locals() else (draw_x + self._shoe_size + 60)

        # Draw shield icon, charges and countdown after the shoe block
        shield_active = (shield_seconds is not None and shield_seconds > 0)
        shield_have = (shield_charges is not None and shield_charges > 0)
        if shield_active or shield_have:
            self._ensure_shield_assets()
            y = self.y0 + max(0, (heart_h - self._shield_size) // 2)
            # Icon
            surface.blit(self._shield_icon, (draw_x, y))
            # Charges text
            charges_txt = f"x{max(0, int(shield_charges or 0))}"
            charges_surf = self._font_small.render(charges_txt, True, (255, 255, 255))
            cx = draw_x + self._shield_size + 10
            cy = y + (self._shield_size - charges_surf.get_height()) // 2
            surface.blit(charges_surf, (cx, cy))
            end2_x = cx + charges_surf.get_width()
            if shield_active:
                secs = int(max(0, shield_seconds))
                text_surf = self._font_small.render(str(secs), True, (255, 255, 255))
                pad_x = 8
                pad_y = 4
                box_w = text_surf.get_width() + pad_x * 2
                box_h = text_surf.get_height() + pad_y * 2
                box_y = y + (self._shield_size - box_h) // 2
                box_x = end2_x + 10
                bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
                bg.fill((0, 0, 0, 140))
                surface.blit(bg, (box_x, box_y))
                surface.blit(text_surf, (box_x + pad_x, box_y + pad_y))
