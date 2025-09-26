from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import Student
from .assign_forms import AssignBedForm
from rooms.models import Bed

class AssignBedView(UpdateView):
    model = Student
    form_class = AssignBedForm
    template_name = 'students/assign_bed.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        bed = form.cleaned_data['bed']
        bed.is_occupied = True
        bed.save()
        self.object.room = bed.room
        return super().form_valid(form)
