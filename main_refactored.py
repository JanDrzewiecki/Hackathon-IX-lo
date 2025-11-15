#!/usr/bin/env python3
"""
Uranek Reactor Run - Refaktoryzowana wersja
Punkt wejścia gry po refaktoryzacji.

Uruchomienie: python3 main_refactored.py
"""

# UWAGA: Ten plik używa STAREGO main.py z zaadaptowanymi importami
# aby szybko uruchomić grę po refaktoryzacji.
# W pełnej wersji należy utworzyć klasę Game w src/core/game.py

import sys
import os

# Dodaj katalog src do PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.dirname(__file__))

# Importuj i uruchom oryginalny main
# (z automatycznie zaktualizowanymi importami)
from game import main

if __name__ == '__main__':
    print("🎮 Uruchamiam Uranek Reactor Run (wersja refaktoryzowana)")
    print("📁 Nowa struktura katalogów: src/core, src/entities, src/managers, src/ui, src/utils")
    print("=" * 60)
    # Uwaga: Stary main.py ma być uruchamiany z katalogu głównego
    # gdzie znajdują się obrazy w folderze 'game/'
