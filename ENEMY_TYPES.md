# System 3 Rodzajów Wrogów - Dokumentacja

## Typy Wrogów

Gra ma **3 typy wrogów** o różnej trudności:

### 1. WEAK (Słaby) - Zielony
- **HP**: 30 (3 strzały × 10 damage)
- **Atak**: 10 damage
- **Prędkość**: 2
- **Liczba**: 6 przeciwników na pokój
- **Kolor**: Jasny zielony (100, 255, 100)
- **Rozmiar**: 32px

### 2. MEDIUM (Średni) - Pomarańczowy
- **HP**: 50 (5 strzałów × 10 damage)
- **Atak**: 15 damage
- **Prędkość**: 2.5
- **Liczba**: 4 przeciwników na pokój
- **Kolor**: Pomarańczowy (255, 200, 100)
- **Rozmiar**: 40px

### 3. STRONG (Mocny) - Czerwony
- **HP**: 80 (8 strzałów × 10 damage)
- **Atak**: 20 damage
- **Prędkość**: 3
- **Liczba**: 2 przeciwników na pokój
- **Kolor**: Czerwony (255, 100, 100)
- **Rozmiar**: 48px

## Jak to działa

### Przypisanie typu do pokoju

Przy **generowaniu gry** (każde uruchomienie):
1. System tworzy 6 pokoi
2. **Każdy pokój losuje typ wroga** (WEAK, MEDIUM lub STRONG)
3. Ten typ pozostaje **stały dla całej sesji gry**

### Przykład layoutu:

```
============================================================
ROOM LAYOUT - Numbered by distance from Room 0
============================================================
  Room [0] (distance: 0) - Enemy: WEAK: top→1, right→2
  Room [1] (distance: 1) - Enemy: MEDIUM: bottom→0
  Room [2] (distance: 1) - Enemy: STRONG: left→0, bottom→3
  Room [3] (distance: 2) - Enemy: WEAK: top→2, right→4
  Room [4] (distance: 2) - Enemy: MEDIUM: left→3, bottom→5
  Room [5] (distance: 3) - Enemy: STRONG: top→4
============================================================
```

### Spawning wrogów

Gdy wchodzisz do pokoju:
1. **Wrogowie są czyszczeni** z poprzedniego pokoju
2. **Spawner resetuje się** dla typu wroga aktualnego pokoju
3. **Spawning rozpoczyna się** - wrogo pojawiają się stopniowo
4. **Maksymalna liczba** zależy od typu:
   - WEAK: max 6 wrogów
   - MEDIUM: max 4 wrogów
   - STRONG: max 2 wrogów

## Rozpoznawanie wrogów w grze

### Po kolorze:
- **Jasnozielone** kwadraty = słabi (łatwo zabić, ale dużo ich)
- **Pomarańczowe** kwadraty = średni (średnia trudność)
- **Czerwone** kwadraty = mocni (trudno zabić, ale tylko 2)

### Po rozmiarze:
- **Małe** (32px) = słabi
- **Średnie** (40px) = średni
- **Duże** (48px) = mocni

### Po zachowaniu:
- **Wolniejsi** = słabi (prędkość 2)
- **Średnio szybcy** = średni (prędkość 2.5)
- **Najszybsi** = mocni (prędkość 3)

## Strategie

### Pokój ze słabymi wrogami (WEAK):
- ✅ Dużo wrogów, ale łatwo padają
- ✅ Dobry na farming punktów
- ⚠️ Uważaj na otoczenie (6 naraz!)

### Pokój ze średnimi wrogami (MEDIUM):
- ⚠️ Zbalansowana trudność
- ⚠️ Silniejszy atak (15 damage)
- ✅ Tylko 4 wrogów

### Pokój z mocnymi wrogami (STRONG):
- ❌ Bardzo trudni do zabicia (8 hitów!)
- ❌ Najmocniejszy atak (20 damage)
- ❌ Najszybsi
- ✅ Ale tylko 2 jednocześnie

## Implementacja

### Pliki:
- **enemy_type.py** - Definicje typów wrogów (EnemyType, EnemyTypeConfig)
- **enemy.py** - Klasa Enemy z obsługą typów
- **enemy_spawner.py** - Spawner używający typów z pokoju
- **room_manager.py** - Przypisanie typu do każdego pokoju

### Kod:
```python
# Przykład: Stworzenie wroga typu STRONG
enemy = Enemy(x, y, EnemyType.STRONG, room_manager)

# Config dla typu
config = EnemyTypeConfig.get_config(EnemyType.MEDIUM)
# config = {'hp': 50, 'ad': 15, 'speed': 2.5, 'count': 4, ...}
```

## Losowość

✅ **Typ wroga dla pokoju losowany przy starcie gry**
✅ **Każde uruchomienie = inny rozkład typów**
✅ **Podczas jednej sesji = stały rozkład**

Możesz mieć różne kombinacje:
- Wszystkie pokoje WEAK (łatwa gra!)
- Mix typów (zbalansowane)
- Wszystkie pokoje STRONG (hardcore!)

