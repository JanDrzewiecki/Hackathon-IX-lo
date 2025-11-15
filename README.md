# Uranek Reactor Run 🎮

A fast-paced action game built with Pygame.

## Authors
- Jan Drzewiecki
- Wiktor Owerczuk
- Witold Cieślinski
- Łukasz Ciskowski

## Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Game
```bash
python3 main.py
```

Or use the start script:
```bash
./start_game.sh
```

## Controls
- **Arrow Keys / WASD** - Move
- **Mouse** - Aim
- **Left Click** - Shoot
- **E** - Activate speed boost
- **ESC** - Pause/Menu

## Project Structure
```
├── main.py                  # Game entry point
├── src/                     # Source code
│   ├── core/               # Core game systems
│   ├── entities/           # Game entities (player, enemies, etc.)
│   ├── managers/           # Resource and game managers
│   ├── ui/                 # User interface components
│   └── utils/              # Utility functions and helpers
├── game/                    # Game assets (images, sprites)
└── backup_original/         # Original game code (backup)
```

## Features
- Dynamic enemy spawning
- Multiple enemy types with different behaviors
- Power-ups (speed boost, shield, strength)
- Boss battles
- Particle effects
- Room-based progression

## Requirements
- Python 3.8+
- Pygame 2.6.1+

---

Enjoy the game! 🚀
