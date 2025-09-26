from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'Reconcile inconsistencies between Bed.student and Student.room. Sets Student.room to the Bed.room when a Bed is assigned to a student.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without saving.')

    def handle(self, *args, **options):
        dry_run = options.get('dry_run')
        from rooms.models import Bed
        from students.models import Student

        fixed_student_rooms = 0
        mismatches = []
        students_with_room_no_bed = []

        self.stdout.write('Starting reconciliation...')

        # Fix students whose bed indicates a different room
        for bed in Bed.objects.select_related('student', 'room').all():
            if bed.student:
                student = bed.student
                room = bed.room
                if student.room_id != room.id:
                    mismatches.append((student.user.username if hasattr(student, 'user') else str(student.id), student.room_id, room.number if room else room))
                    if not dry_run:
                        student.room = room
                        student.save(update_fields=['room'])
                    fixed_student_rooms += 1

        # Find students that have a room set but currently are not assigned to any Bed
        for student in Student.objects.select_related('user', 'room').all():
            has_bed = Bed.objects.filter(student=student).exists()
            if student.room_id and not has_bed:
                students_with_room_no_bed.append((student.user.username if hasattr(student, 'user') else str(student.id), student.room.number if student.room else None))

        self.stdout.write('\nSummary:')
        self.stdout.write(f'  Total mismatched student->room corrected: {fixed_student_rooms} (dry-run={dry_run})')
        if mismatches:
            self.stdout.write('\n  Detailed fixes:')
            for username, old_room_id, new_room in mismatches:
                self.stdout.write(f'    - {username}: {old_room_id} -> {new_room}')

        if students_with_room_no_bed:
            self.stdout.write('\n  Students with a room set but no bed assignment:')
            for username, room_number in students_with_room_no_bed:
                self.stdout.write(f'    - {username}: room {room_number}')

        self.stdout.write('\nReconciliation complete.')
