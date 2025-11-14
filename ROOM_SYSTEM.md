# System 6 Pokoi - Dokumentacja

## Jak to działa

### Generowanie pokoi przy starcie gry

Za każdym razem gdy uruchamiasz grę (`python game/main.py`), system:

1. **Tworzy 6 pustych pokoi** (numerowanych 0-5)
2. **Losowo łączy je** za pomocą korytarzy (top, bottom, left, right)
3. **Zapewnia że wszystkie pokoje są osiągalne** - można dotrzeć do każdego z pokoju 0
4. **Nie wszystkie pokoje mają 4 korytarze** - niektóre mają 1, inne 2, 3 lub 4

### Wyświetlanie schematu

Przy starcie gry w konsoli zobaczysz:

```
============================================================
ROOM LAYOUT - Numbered by distance from Room 0
============================================================
  Room [0] (distance: 0): top→1, right→2
  Room [1] (distance: 1): bottom→0, right→3
  Room [2] (distance: 1): left→0, bottom→4
  Room [3] (distance: 2): left→1, bottom→5
  Room [4] (distance: 2): top→2, right→5
  Room [5] (distance: 3): top→3, left→4
============================================================
```

To oznacza:
- **Room [0]** (START, odl. 0) - ma korytarze: w górę do pokoju 1, w prawo do pokoju 2
- **Room [1]** (odl. 1) - ma korytarze: w dół do pokoju 0, w prawo do pokoju 3
- **Room [5]** (NAJDALSZY, odl. 3) - ma korytarze: w górę do pokoju 3, w lewo do pokoju 4

### Przykład wizualizacji

Dla powyższego layoutu, struktura wygląda tak:

```
        [2]
         ↓
        [5]
       ↙ ↓
    [3]  [4]
     ↓  ↙ ↑
    [0]→[1]
```

### W grze

- **Lewy górny róg** pokazuje:
  - `Room: 0` - aktualny pokój
  - `Visited: [0, 1, 3]` - pokoje które już odwiedziłeś

- **Korytarze** - widoczne tylko te które prowadzą do innych pokoi
- **Teleportacja** - gdy dojdziesz do krawędzi ekranu przez korytarz, teleportujesz się do połączonego pokoju

### Gwarancje

✅ **Zawsze 6 pokoi**
✅ **Losowy układ przy każdym uruchomieniu**
✅ **Wszystkie pokoje osiągalne z pokoju 0**
✅ **Wszystkie połączenia obustronne** (jeśli z A do B, to też z B do A)
✅ **Układ NIE zmienia się podczas gry**

### Przykładowe układy

**Układ 1 - liniowy:**
```
Room [0]: right→1
Room [1]: left→0, right→2
Room [2]: left→1, right→3
Room [3]: left→2, right→4
Room [4]: left→3, right→5
Room [5]: left→4
```

**Układ 2 - gwiaździsty:**
```
Room [0]: top→1, bottom→2, left→3, right→4
Room [1]: bottom→0
Room [2]: top→0
Room [3]: right→0, bottom→5
Room [4]: left→0
Room [5]: top→3
```

**Układ 3 - mieszany:**
```
Room [0]: top→3, right→1
Room [1]: left→0, bottom→4
Room [2]: top→5
Room [3]: bottom→0, left→4
Room [4]: top→1, right→3, bottom→5
Room [5]: top→2, bottom→4
```

## Uruchomienie

```bash
cd /Users/lukaszdrzewiecki/PycharmProjects/Hackathon-IX-lo
python3.13 game/main.py
```

Przy każdym uruchomieniu zobaczysz w konsoli inny schemat pokoi!

