from django.urls import path
from .views import ComplaintListView, PaymentListView, StudentListView, RoomListView, VisitorLogListView

urlpatterns = [
    path('complaints/', ComplaintListView.as_view(), name='admin_complaint_list'),
    path('payments/', PaymentListView.as_view(), name='admin_payment_list'),
    path('students/', StudentListView.as_view(), name='admin_student_list'),
    path('rooms/', RoomListView.as_view(), name='admin_room_list'),
    path('visitorlogs/', VisitorLogListView.as_view(), name='admin_visitorlog_list'),
]
