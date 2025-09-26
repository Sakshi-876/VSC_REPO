
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Room, Bed
from .forms import BedAssignmentForm

class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'rooms/room_list.html'


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class BedAssignmentView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Bed
    form_class = BedAssignmentForm
    template_name = 'rooms/assign_bed.html'
    success_url = reverse_lazy('manage_beds')
