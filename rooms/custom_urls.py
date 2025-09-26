from django.urls import path
from .custom_views import (
    RoomListView, RoomCreateView, RoomUpdateView, RoomDeleteView,
    BedListView, BedCreateView, BedUpdateView, BedDeleteView
)

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='room_list_custom'),
    path('rooms/add/', RoomCreateView.as_view(), name='room_add'),
    path('rooms/<int:pk>/edit/', RoomUpdateView.as_view(), name='room_edit'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),
    path('beds/', BedListView.as_view(), name='bed_list'),
    path('beds/add/', BedCreateView.as_view(), name='bed_add'),
    path('beds/<int:pk>/edit/', BedUpdateView.as_view(), name='bed_edit'),
    path('beds/<int:pk>/delete/', BedDeleteView.as_view(), name='bed_delete'),
]
