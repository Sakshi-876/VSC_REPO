from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Room, Bed

# Room Views
class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'rooms/room_list_custom.html'

class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    fields = ['number', 'capacity', 'is_available']
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('room_list_custom')

class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    fields = ['number', 'capacity', 'is_available']
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('room_list_custom')

class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'rooms/room_confirm_delete.html'
    success_url = reverse_lazy('room_list_custom')

# Bed Views
class BedListView(LoginRequiredMixin, ListView):
    model = Bed
    template_name = 'rooms/bed_list.html'

class BedCreateView(LoginRequiredMixin, CreateView):
    model = Bed
    fields = ['room', 'bed_number', 'is_occupied']
    template_name = 'rooms/bed_form.html'
    success_url = reverse_lazy('bed_list')

class BedUpdateView(LoginRequiredMixin, UpdateView):
    model = Bed
    fields = ['room', 'bed_number', 'is_occupied']
    template_name = 'rooms/bed_form.html'
    success_url = reverse_lazy('bed_list')

class BedDeleteView(DeleteView):
    model = Bed
    template_name = 'rooms/bed_confirm_delete.html'
    success_url = reverse_lazy('bed_list')
