from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import TemplateView
from hostel_management.models import Complaint, Payment
from students.models import Student
from rooms.models import Room, Bed

class AdminDashboardView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        alerts = []
        if Complaint.objects.filter(status='Pending').exists():
            alerts.append('There are pending complaints to review.')
        if Payment.objects.filter(status='Due').exists():
            alerts.append('There are due payments.')
        if Bed.objects.filter(is_occupied=False).count() == 0:
            alerts.append('All beds are currently occupied!')
        if Room.objects.filter(is_available=True).count() == 0:
            alerts.append('No available rooms!')
        context['alerts'] = alerts
        context['user'] = self.request.user
        return context
