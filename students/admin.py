from django.contrib import admin
from .models import Student
from .models import RoomApplication
from django.utils import timezone
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.contrib import messages
from rooms.models import Bed

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'room')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']


@admin.register(RoomApplication)
class RoomApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'status', 'created_at', 'reviewed_at', 'reviewed_by')
    list_filter = ('status', 'created_at')
    search_fields = ['student__user__username', 'student__student_id', 'reason']
    readonly_fields = ('created_at',)
    actions = ['approve_applications', 'reject_applications']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve-selected/', self.admin_site.admin_view(self.approve_with_options_view), name='approve_selected'),
        ]
        return custom_urls + urls

    def approve_with_options(self, request, queryset):
        """Action that redirects to an intermediate page where admin can choose auto-assign or manually pick beds."""
        ids = ",".join(str(pk) for pk in queryset.values_list('pk', flat=True))
        return HttpResponseRedirect(f"approve-selected/?ids={ids}")

    approve_with_options.short_description = 'Approve selected with options (auto or manual select)'

    def approve_applications(self, request, queryset):
        assigned = 0
        unassigned = 0
        for app in queryset.select_related('student'):
            # Try to find a free bed
            try:
                bed = Bed.objects.filter(is_occupied=False, room__is_available=True).select_related('room').first()
            except Exception:
                bed = None

            if bed:
                # Assign student to bed and mark occupied
                bed.student = app.student
                bed.is_occupied = True
                bed.save()
                # Update student's room FK
                app.student.room = bed.room
                app.student.save(update_fields=['room'])
                app.status = 'Approved'
                app.reviewed_at = timezone.now()
                app.reviewed_by = request.user
                app.save()
                assigned += 1
            else:
                # No bed available; still mark approved but note unassigned
                app.status = 'Approved'
                app.reviewed_at = timezone.now()
                app.reviewed_by = request.user
                app.save()
                unassigned += 1

        total = assigned + unassigned
        self.message_user(request, f"{total} application(s) processed: {assigned} assigned, {unassigned} unassigned (no available bed).")
    approve_applications.short_description = 'Mark selected applications as Approved'

    def reject_applications(self, request, queryset):
        updated = queryset.update(status='Rejected', reviewed_at=timezone.now(), reviewed_by=request.user)
        self.message_user(request, f"{updated} application(s) marked as Rejected.")
    reject_applications.short_description = 'Mark selected applications as Rejected'

    def approve_with_options_view(self, request):
        """Admin view to approve selected RoomApplications with options to auto-assign or pick beds."""
        ids = request.GET.get('ids') or request.POST.get('ids')
        if not ids:
            self.message_user(request, "No applications selected.", level=messages.ERROR)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '../'))

        id_list = [int(x) for x in ids.split(',') if x]
        applications = list(self.model.objects.filter(pk__in=id_list).select_related('student'))

        available_beds = Bed.objects.filter(is_occupied=False, room__is_available=True).select_related('room')

        if request.method == 'POST':
            # Process form submission
            action = request.POST.get('action')
            if action == 'auto':
                assigned = 0
                unassigned = 0
                for app in applications:
                    bed = Bed.objects.filter(is_occupied=False, room__is_available=True).first()
                    if bed:
                        bed.student = app.student
                        bed.is_occupied = True
                        bed.save()
                        app.student.room = bed.room
                        app.student.save(update_fields=['room'])
                        app.status = 'Approved'
                        app.reviewed_at = timezone.now()
                        app.reviewed_by = request.user
                        app.save()
                        assigned += 1
                    else:
                        app.status = 'Approved'
                        app.reviewed_at = timezone.now()
                        app.reviewed_by = request.user
                        app.save()
                        unassigned += 1
                self.message_user(request, f"{len(applications)} processed: {assigned} assigned, {unassigned} unassigned.")
                return HttpResponseRedirect('../../')

            if action == 'manual':
                # Expected POST data: mapping of application_<pk> -> bed_id or empty
                processed = 0
                for app in applications:
                    key = f"application_{app.pk}"
                    bed_id = request.POST.get(key)
                    if bed_id:
                        try:
                            bed = Bed.objects.get(pk=int(bed_id), is_occupied=False, room__is_available=True)
                        except Bed.DoesNotExist:
                            bed = None

                        if bed:
                            bed.student = app.student
                            bed.is_occupied = True
                            bed.save()
                            app.student.room = bed.room
                            app.student.save(update_fields=['room'])
                            app.status = 'Approved'
                            app.reviewed_at = timezone.now()
                            app.reviewed_by = request.user
                            app.save()
                            processed += 1
                        else:
                            # mark as approved but unassigned
                            app.status = 'Approved'
                            app.reviewed_at = timezone.now()
                            app.reviewed_by = request.user
                            app.save()
                self.message_user(request, f"{len(applications)} processed; {processed} assigned manually.")
                return HttpResponseRedirect('../../')

        context = {
            **self.admin_site.each_context(request),
            'applications': applications,
            'available_beds': available_beds,
            'ids': ids,
        }
        return TemplateResponse(request, 'admin/students/approve_with_options.html', context)
