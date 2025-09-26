
from django.urls import path
from .views import RoomListView, BedAssignmentView

urlpatterns = [
    path('', RoomListView.as_view(), name='room_list'),
    path('assign-bed/<int:pk>/', BedAssignmentView.as_view(), name='assign_bed'),
]
