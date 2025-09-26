from django import forms
from .models import Student
from rooms.models import Bed

class AssignBedForm(forms.ModelForm):
    bed = forms.ModelChoiceField(queryset=Bed.objects.filter(is_occupied=False), required=True)

    class Meta:
        model = Student
        fields = ['bed']
