

app_name = 'students'
from django.urls import path

from .views import StudentLoginView, StudentLogoutView
from .student_views import StudentDashboardView, ComplaintCreateView
from .student_views import ApplyRoomView
from .signup_views import StudentSignUpView
from .edit_views import StudentUpdateView, StudentListView
from .assign_views import AssignBedView

urlpatterns = [
    path('login/', StudentLoginView.as_view(), name='login'),
    path('logout/', StudentLogoutView.as_view(), name='logout'),
    path('signup/', StudentSignUpView.as_view(), name='signup'),
    path('dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('complaint/new/', ComplaintCreateView.as_view(), name='student_complaint_new'),
    path('apply-room/', ApplyRoomView.as_view(), name='apply_room'),
    path('edit/<int:pk>/', StudentUpdateView.as_view(), name='student_edit'),
    path('residents/', StudentListView.as_view(), name='student_list'),
    path('assign-bed/<int:pk>/', AssignBedView.as_view(), name='assign_bed'),
]
