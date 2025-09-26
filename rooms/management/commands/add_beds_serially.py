from django.core.management.base import BaseCommand
from rooms.models import Room, Bed

class Command(BaseCommand):
    help = 'Serially add beds to each room as per its capacity.'

    def handle(self, *args, **options):
        created_count = 0
        for room in Room.objects.all():
            existing_beds = room.beds.count()
            for i in range(existing_beds + 1, room.capacity + 1):
                bed_number = f'B{i}'
                Bed.objects.create(room=room, bed_number=bed_number)
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully added {created_count} beds serially as per room capacity.'))
