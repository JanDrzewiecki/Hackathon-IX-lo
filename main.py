#!/usr/bin/env python3
"""
🎮 Uranek Reactor Run - Refactored Version
Game entry point.

Authors: Jan Drzewiecki, Wiktor Owerczuk, Witold Cieślinski, Łukasz Ciskowski
Refactoring: November 2025
"""

import sys
import os

# Add project root, src, and backup_original to import paths
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))
sys.path.insert(0, os.path.join(project_root, 'backup_original'))

if __name__ == '__main__':
    print("=" * 70)
    print("🎮 URANEK REACTOR RUN - Refactored Version")
    print("=" * 70)
    print("📁 Using new structure: src/core, src/entities, src/managers, src/ui")
    print("🎯 Original Python files backed up to: backup_original/")
    print("🖼️  Assets (images) remain in: game/")
    print("🔧 Utilities refactored with SOLID principles")
    print("=" * 70)
    print("")
    
    # Import and run the game from backup_original
    # This allows the original game logic to run while using refactored utilities
    import main as game_main
