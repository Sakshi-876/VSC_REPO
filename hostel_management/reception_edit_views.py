from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import VisitorLog
from .reception_views import AdminOnlyRequiredMixin

class VisitorLogUpdateView(AdminOnlyRequiredMixin, UpdateView):
    model = VisitorLog
    fields = ['student', 'visitor_name', 'check_in', 'check_out', 'purpose']
    template_name = 'reception/visitorlog_form.html'
    success_url = reverse_lazy('reception_visitorlog_list')

class VisitorLogDeleteView(AdminOnlyRequiredMixin, DeleteView):
    model = VisitorLog
    template_name = 'reception/visitorlog_confirm_delete.html'
    success_url = reverse_lazy('reception_visitorlog_list')
