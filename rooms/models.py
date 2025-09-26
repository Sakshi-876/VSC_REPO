
from django.db import models

class Room(models.Model):
    def update_beds_status(self):
        # Update all beds' is_occupied status based on student assignment
        for bed in self.beds.all():
            bed.is_occupied = bool(bed.student)
            bed.save(update_fields=["is_occupied"])
        self.update_availability()

    def update_availability(self):
        total_beds = self.beds.count()
        occupied_beds = self.beds.filter(is_occupied=True).count()
        self.is_available = occupied_beds < total_beds
        self.save(update_fields=["is_available"])
    number = models.CharField(max_length=10)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.number



class Bed(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=10)
    is_occupied = models.BooleanField(default=False)
    student = models.OneToOneField('students.Student', on_delete=models.SET_NULL, null=True, blank=True, unique=True)

    def __str__(self):
        return f"Bed {self.bed_number} in Room {self.room.number}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Prevent adding more beds than room capacity
        if self.room and self.room.beds.exclude(pk=self.pk).count() >= self.room.capacity:
            raise ValidationError({
                'room': "You cannot assign more beds than the room's capacity. Please increase the room capacity or remove an existing bed."
            })
        # Ensure only one bed per student
        if self.student and Bed.objects.filter(student=self.student).exclude(pk=self.pk).exists():
            raise ValidationError({
                'student': "This student is already assigned to another bed."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        # Determine previous student (if any) so we can clear their room if changed
        previous_student = None
        if self.pk:
            try:
                previous = Bed.objects.get(pk=self.pk)
                previous_student = previous.student
            except Bed.DoesNotExist:
                previous_student = None

        self.is_occupied = bool(self.student)
        super().save(*args, **kwargs)

        # Sync Student.room for new assignment
        try:
            Student = __import__('students.models', fromlist=['Student']).Student
        except Exception:
            Student = None

        if Student and self.student:
            # Assign this bed's room to the student if not set
            if getattr(self.student, 'room_id', None) != self.room.id:
                self.student.room = self.room
                self.student.save(update_fields=['room'])

        # If the bed was previously assigned to a different student, clear that student's room
        if Student and previous_student and previous_student != self.student:
            # Only clear if their room points to this bed's room
            try:
                if getattr(previous_student, 'room_id', None) == self.room.id:
                    previous_student.room = None
                    previous_student.save(update_fields=['room'])
            except Exception:
                pass

        # Update room's availability after saving bed
        self.room.update_availability()

    def delete(self, *args, **kwargs):
        room = self.room
        super().delete(*args, **kwargs)
        room.update_availability()

    def update_room_availability(self, room=None):
        room = room or self.room
        total_beds = room.beds.count()
        occupied_beds = room.beds.filter(is_occupied=True).count()
        room.is_available = occupied_beds < total_beds
        room.save(update_fields=["is_available"])
