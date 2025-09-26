





from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LogoutView
from .models import Complaint, Payment, VisitorLog
from students.models import Student
from rooms.models import Room
from django.urls import reverse_lazy

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class ComplaintListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Complaint
    template_name = 'admin/complaint_list.html'

class PaymentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Payment
    template_name = 'admin/payment_list.html'

class StudentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Student
    template_name = 'admin/student_list.html'

class RoomListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Room
    template_name = 'admin/room_list.html'

class VisitorLogListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = VisitorLog
    template_name = 'admin/visitorlog_list.html'

# Homepage view
class HomePageView(TemplateView):
    template_name = 'index.html'

# About Us page view
class AboutUsView(TemplateView):
    template_name = 'about_us.html'


# Staff Logout View with message
from django.contrib import messages
from django.shortcuts import redirect

class StaffLogoutView(LogoutView):
    template_name = 'logout.html'
    http_method_names = ['get', 'post', 'head', 'options']
    def dispatch(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        logout(request)
        messages.success(request, "You have been securely logged out. Thank you for using the Hostel Management System.")
        return super().dispatch(request, *args, **kwargs)
