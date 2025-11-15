"""
Stałe konfiguracyjne gry.
"""

# Ustawienia ekranu
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Obszar gry
GAME_AREA_WIDTH = 800
GAME_AREA_HEIGHT = 600

# Rozmiary obiektów
ENEMY_SIZE = 10
BULLET_SIZE = 8

# Ustawienia gracza (Uranek)
URANEK_FRAME_WIDTH = 200
URANEK_FRAME_HEIGHT = 200
URANEK_SCALE = 0.7
URANEK_SIZE = (int(URANEK_FRAME_WIDTH * URANEK_SCALE), int(URANEK_FRAME_HEIGHT * URANEK_SCALE))

# Ścieżki do zasobów
ASSETS_DIR = "game"  # Folder z assetami (obrazy, sprite'y)

# Kolory
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GOLD = (255, 215, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_YELLOW = (255, 255, 0)

# Parametry gry
HP_PER_HEART = 20  # Ilość HP reprezentowana przez jedno serce
POWERUP_SIZE = 48  # Rozmiar power-upów (buty, tarcza, siła)

# Czas trwania power-upów (w sekundach)
SPEED_BOOST_DURATION = 5
SHIELD_DURATION = 3
STRENGTH_DURATION = 3

# Ilość ładunków power-upów po podniesieniu
SPEED_BOOST_CHARGES = 3
SHIELD_CHARGES = 3
STRENGTH_CHARGES = 2
