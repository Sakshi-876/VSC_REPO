from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView
from .models import Student

class StudentUpdateView(UpdateView):
    model = Student
    fields = ['student_id', 'contact', 'photo', 'room']
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
