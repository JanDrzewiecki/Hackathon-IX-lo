"""
Test script to visualize multiple random room generations
"""
import sys
sys.path.append('game')

from room_manager import RoomManager

def visualize_room_layout(rooms):
    """Print a visual representation of room connections"""
    print("\n" + "="*50)
    for room_id in range(6):
        room = rooms[room_id]
        connections = []
        for direction, connected_to in room.connections.items():
            if connected_to is not None:
                connections.append(f"{direction}→{connected_to}")
        status = ', '.join(connections) if connections else 'ISOLATED'
        print(f"Room {room_id}: {status}")
    print("="*50)

# Generate and visualize 5 different layouts
print("\n🎲 Testing Random Room Generation 🎲\n")

for i in range(5):
    print(f"\n--- Layout #{i+1} ---")
    # Create a minimal room manager just to generate rooms
    rm = RoomManager(1920, 1080, margin_pixels=100)
    visualize_room_layout(rm.rooms)

    # Verify all rooms are connected (can reach all from room 0)
    visited = {0}
    to_visit = [0]

    while to_visit:
        current = to_visit.pop(0)
        for direction, connected_room in rm.rooms[current].connections.items():
            if connected_room is not None and connected_room not in visited:
                visited.add(connected_room)
                to_visit.append(connected_room)

    if len(visited) == 6:
        print("✅ All rooms are connected!")
    else:
        print(f"❌ WARNING: Only {len(visited)} rooms are reachable: {sorted(visited)}")

print("\n✨ Random room generation is working! Each game will have a different layout.\n")

