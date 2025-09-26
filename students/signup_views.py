from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .models import Student
from rooms.models import Room
from django import forms



class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    student_id = forms.CharField(max_length=20, required=True)
    contact = forms.CharField(max_length=20, required=False)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'students/signup.html'
    success_url = reverse_lazy('students:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.save()
        student_id = form.cleaned_data.get('student_id')
        contact = form.cleaned_data.get('contact')
        photo = form.cleaned_data.get('photo')
        from django.db import IntegrityError
        try:
            Student.objects.create(user=user, student_id=student_id, contact=contact, photo=photo)
        except IntegrityError:
            form.add_error('student_id', 'This Student ID is already registered. Please use a unique Student ID.')
            user.delete()
            return self.form_invalid(form)
        return response
