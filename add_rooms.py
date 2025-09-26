from rooms.models import Room

# Add 20+ sample rooms
def add_rooms():
    rooms = [
        Room(number=f'R{str(i).zfill(3)}', capacity=(2 + i % 4)) for i in range(1, 26)
    ]
    Room.objects.bulk_create(rooms)
    print(f"Added {len(rooms)} rooms.")

if __name__ == "__main__":
    add_rooms()
