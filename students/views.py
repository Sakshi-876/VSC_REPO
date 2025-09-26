
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib import messages
from students.models import Student

class StudentLoginView(LoginView):
    template_name = 'students/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not Student.objects.filter(user=user).exists():
            messages.error(self.request, "No student profile found for this account. Please sign up first.")
            return self.form_invalid(form)
        return super().form_valid(form)

class StudentLogoutView(LogoutView):
    next_page = '/'
