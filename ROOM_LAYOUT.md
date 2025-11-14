# Room Layout Documentation

## Fixed Room Schema

The game has a **FIXED** layout of 6 rooms that **NEVER CHANGES** - not between game sessions, not during gameplay.

### Visual Map:
```
      [2]
       |
  [3]-[0]-[1]
       |
      [4]
       |
      [5]
```

### Room Connections:
```
Room 0 (center):  top→2, bottom→4, left→3, right→1
Room 1 (right):   left→0
Room 2 (top):     bottom→0
Room 3 (left):    right→0
Room 4 (middle):  top→0, bottom→5
Room 5 (bottom):  top→4
```

### How It Works:
- **Starting Room**: Always Room 0 (center)
- **Total Rooms**: 6 (numbered 0-5)
- **Layout**: Hardcoded, never changes
- **Bidirectional**: All connections are two-way

### Example Paths:
- Room 0 → top → Room 2 → bottom → Room 0 (back where you started)
- Room 0 → bottom → Room 4 → bottom → Room 5 (deepest room)
- Room 0 → left → Room 3 → right → Room 0 (back)
- Room 0 → right → Room 1 → left → Room 0 (back)

### Navigation Rules:
1. You can only move through corridors that exist
2. If you go "top" from Room A to Room B, you return via "bottom" from Room B
3. The layout NEVER changes during the game
4. Each room shows only its active corridors (no fake exits)

### In-Game Features:
- Top-left corner shows: `Room: X` (current room number)
- Below that: `Visited: [0, 1, 3, ...]` (list of rooms you've visited)
- When you enter a new room, you see a cyan notification with the room number

