
from django.contrib import admin
from django.utils.html import format_html
from .models import Room, Bed
@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('bed_number', 'room', 'is_occupied', 'student', 'bed_actions')
    list_filter = ('room', 'is_occupied')
    search_fields = ('bed_number', 'student__name')
    autocomplete_fields = ['student']

    def bed_actions(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        edit_url = reverse('admin:rooms_bed_change', args=[obj.pk])
        delete_url = reverse('admin:rooms_bed_delete', args=[obj.pk])
        return format_html(
            '<a href="{}">Edit</a> | <a href="{}">Delete</a>',
            edit_url, delete_url
        )
    bed_actions.short_description = 'Actions'

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'is_available', 'room_actions')

    def room_actions(self, obj):
        edit_url = f'/admin/rooms/room/{obj.pk}/change/'
        delete_url = f'/admin/rooms/room/{obj.pk}/delete/'
        return format_html(
            '<a href="{}">Edit</a> | <a href="{}">Delete</a>',
            edit_url, delete_url
        )
    room_actions.short_description = 'Actions'
