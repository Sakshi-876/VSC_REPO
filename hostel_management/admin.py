
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Complaint, Payment, VisitorLog

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'status', 'created_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'status', 'due_date', 'paid_at', 'payment_actions')

    def payment_actions(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        edit_url = reverse('admin:hostel_management_payment_change', args=[obj.pk])
        delete_url = reverse('admin:hostel_management_payment_delete', args=[obj.pk])
        return format_html(
            '<a href="{}">Edit</a> | <a href="{}">Delete</a>',
            edit_url, delete_url
        )
    payment_actions.short_description = 'Actions'

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'visitor_name', 'check_in', 'check_out', 'purpose')
