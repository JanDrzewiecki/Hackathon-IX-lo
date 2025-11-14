python3.13 test_rooms_simple.py# Vampire Survivor - Room System Game

## Uruchamianie gry

### Metoda 1: Z terminala (CMD/PowerShell/Terminal)

```bash
cd /Users/lukaszdrzewiecki/PycharmProjects/Hackathon-IX-lo
python3.13 game/main.py
```

### Metoda 2: Skrypt uruchomieniowy (macOS/Linux)

```bash
cd /Users/lukaszdrzewiecki/PycharmProjects/Hackathon-IX-lo
chmod +x run_game.sh
./run_game.sh
```

### Metoda 3: Z IDE (PyCharm)

1. Otwórz projekt w PyCharm
2. Kliknij prawym przyciskiem na `game/main.py`
3. Wybierz "Run 'main'"

## Sterowanie

- **WASD** - Ruch gracza
- **Mysz (LPM)** - Strzał
- **ESC** - Wyjście z gry

## System pokoi

Gra ma **6 pokoi** w stałym układzie:

```
      [2]
       |
  [3]-[0]-[1]
       |
      [4]
       |
      [5]
```

- Zaczynasz w pokoju 0 (centrum)
- Każdy pokój ma różną liczbę wyjść (korytarzy)
- Układ **NIE ZMIENIA SIĘ** podczas gry ani między sesjami
- Wszystkie połączenia są obustronne

Zobacz `ROOM_LAYOUT.md` dla szczegółów.

## Wymagania

- Python 3.13
- pygame 2.6.1+

Instalacja zależności:
```bash
pip install -r requirements.txt
```

## Struktura projektu

```
game/
  ├── main.py          - Główna pętla gry
  ├── room_manager.py  - System pokoi i korytarzy
  ├── player.py        - Klasa gracza
  ├── enemy.py         - Klasa wroga
  ├── enemy_spawner.py - Spawner wrogów
  ├── bullet.py        - Klasa pocisku
  ├── notification.py  - Powiadomienia na ekranie
  └── settings.py      - Konfiguracja gry
```

## Debugowanie

Jeśli gra się nie uruchamia:

1. Sprawdź czy masz zainstalowane pygame:
   ```bash
   python3.13 -m pip list | grep pygame
   ```

2. Jeśli brak, zainstaluj:
   ```bash
   python3.13 -m pip install pygame
   ```

3. Sprawdź wersję Pythona:
   ```bash
   python3.13 --version
   ```

4. Uruchom z pełną ścieżką:
   ```bash
   /usr/local/bin/python3.13 /Users/lukaszdrzewiecki/PycharmProjects/Hackathon-IX-lo/game/main.py
   ```

