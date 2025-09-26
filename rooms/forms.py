from django import forms
from rooms.models import Bed
from students.models import Student

class BedAssignmentForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=Student.objects.filter(bed__isnull=True),
        required=True,
        label="Student (without bed)"
    )
    class Meta:
        model = Bed
        fields = ['room', 'bed_number', 'student']

    def clean_student(self):
        student = self.cleaned_data['student']
        if Bed.objects.filter(student=student).exists():
            raise forms.ValidationError("This student is already assigned to a bed.")
        return student

    def clean(self):
        cleaned_data = super().clean()
        bed = self.instance
        if bed.student and Bed.objects.filter(student=bed.student).exclude(pk=bed.pk).exists():
            self.add_error('student', "This student is already assigned to another bed.")
        return cleaned_data
