"""
Simple test to verify room connections are correct
"""
import sys
sys.path.append('game')

from room_manager import RoomManager

# Create room manager
rm = RoomManager(1920, 1080, margin_pixels=100)

print("\n=== ROOM CONNECTIONS ===")
for room_id in range(6):
    room = rm.rooms[room_id]
    print(f"\nRoom {room_id}:")
    for direction, connected_to in room.connections.items():
        if connected_to is not None:
            print(f"  {direction} → Room {connected_to}")
            # Verify bidirectional
            opposite = rm.opposite[direction]
            reverse = rm.rooms[connected_to].connections[opposite]
            if reverse == room_id:
                print(f"    ✓ Room {connected_to}.{opposite} → Room {room_id}")
            else:
                print(f"    ❌ ERROR: Room {connected_to}.{opposite} → Room {reverse} (expected {room_id})")

print("\n=== TESTING TRANSITIONS ===")
print("\nFixed Layout Structure:")
print("      [2]")
print("       |")
print("  [3]-[0]-[1]")
print("       |")
print("      [4]")
print("       |")
print("      [5]")
print()

# Test the fixed layout
test_cases = [
    # Starting from room 0
    (0, 'top', 2, "Room 0 → top → Room 2"),
    (0, 'bottom', 4, "Room 0 → bottom → Room 4"),
    (0, 'left', 3, "Room 0 → left → Room 3"),
    (0, 'right', 1, "Room 0 → right → Room 1"),

    # Test bidirectional from room 2
    (2, 'bottom', 0, "Room 2 → bottom → Room 0 (back)"),

    # Test path: 0 → top → 2, then 2 → bottom → 0, then 0 → right → 1
    (1, 'left', 0, "Room 1 → left → Room 0 (back)"),

    # Test path: 0 → bottom → 4 → bottom → 5
    (4, 'bottom', 5, "Room 4 → bottom → Room 5"),
    (5, 'top', 4, "Room 5 → top → Room 4 (back)"),
]

all_passed = True
for from_room, direction, expected_to_room, description in test_cases:
    rm.current_room_id = from_room
    rm.current_room = rm.rooms[from_room]

    actual_to_room = rm.current_room.connections[direction]

    if actual_to_room == expected_to_room:
        print(f"✓ {description}")
    else:
        print(f"❌ {description} - FAILED: got Room {actual_to_room}")
        all_passed = False

if all_passed:
    print("\n✅ All tests passed! Room connections are correct.")
else:
    print("\n❌ Some tests failed!")

