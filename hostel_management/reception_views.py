from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from hostel_management.models import VisitorLog
from students.models import Student


# Only allow admin (superuser) to access reception views
class AdminOnlyRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class VisitorLogListView(AdminOnlyRequiredMixin, LoginRequiredMixin, ListView):
    model = VisitorLog
    template_name = 'reception/visitorlog_list.html'

class VisitorLogCreateView(AdminOnlyRequiredMixin, LoginRequiredMixin, CreateView):
    model = VisitorLog
    fields = ['student', 'visitor_name', 'check_in', 'check_out', 'purpose']
    template_name = 'reception/visitorlog_form.html'
    success_url = reverse_lazy('reception_visitorlog_list')
