from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy
from hostel_management.models import Complaint, Payment
from .models import Student, RoomApplication
from django.views.generic.edit import FormView
from django import forms
from django.contrib import messages

class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'students/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            student = Student.objects.get(user=self.request.user)
            context['student'] = student
            context['room'] = student.room
            # Find assigned bed for this student
            from rooms.models import Bed
            assigned_bed = None
            if student.room:
                try:
                    assigned_bed = Bed.objects.get(student=student)
                except Bed.DoesNotExist:
                    assigned_bed = None
            context['assigned_bed'] = assigned_bed
            context['payments'] = Payment.objects.filter(student=student)
            context['complaints'] = Complaint.objects.filter(student=student)
            context['applications'] = RoomApplication.objects.filter(student=student)
            alerts = []
            if context['complaints'].filter(status='Pending').exists():
                alerts.append('You have pending complaints.')
            if context['payments'].filter(status='Due').exists():
                alerts.append('You have due payments.')
            if not student.room:
                alerts.append('You have not been assigned a room yet.')
            elif not context['assigned_bed']:
                alerts.append('You have not been assigned a bed yet.')
            context['alerts'] = alerts
        except Student.DoesNotExist:
            context['student'] = None
            context['room'] = None
            context['assigned_bed'] = None
            context['payments'] = []
            context['complaints'] = []
            context['applications'] = []
            context['alerts'] = ['No student profile found for your account. Please contact staff or sign up as a student.']
        return context

class ComplaintCreateView(LoginRequiredMixin, CreateView):
    model = Complaint
    fields = ['title', 'description']
    template_name = 'students/complaint_form.html'
    success_url = reverse_lazy('students:student_dashboard')

    def form_valid(self, form):
        form.instance.student = Student.objects.get(user=self.request.user)
        return super().form_valid(form)


class ApplyRoomForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows':4}), required=True, label='Why do you need a room?')


class ApplyRoomView(LoginRequiredMixin, FormView):
    template_name = 'students/apply_room.html'
    form_class = ApplyRoomForm
    success_url = reverse_lazy('students:student_dashboard')

    def form_valid(self, form):
        # Minimal handling: create a Complaint-like record or a simple message.
        # For now, we'll store the application as a Complaint with a special title so staff can view it,
        # or simply show a success message and redirect. This is low-risk and non-invasive.
        try:
            student = Student.objects.get(user=self.request.user)
            # Prevent duplicate pending applications
            if RoomApplication.objects.filter(student=student, status='Pending').exists():
                messages.warning(self.request, 'You already have a pending room application. Please wait for staff review.')
                return super().form_invalid(form)

            RoomApplication.objects.create(student=student, reason=form.cleaned_data['reason'])
        except Student.DoesNotExist:
            messages.error(self.request, 'Student profile not found. Cannot submit room application.')
            return super().form_invalid(form)

        messages.success(self.request, 'Your room application has been submitted. Staff will contact you.')
        return super().form_valid(form)
