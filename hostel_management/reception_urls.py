from django.urls import path
from .reception_views import VisitorLogListView, VisitorLogCreateView
from .reception_edit_views import VisitorLogUpdateView, VisitorLogDeleteView

urlpatterns = [
    path('visitorlogs/', VisitorLogListView.as_view(), name='reception_visitorlog_list'),
    path('visitorlogs/new/', VisitorLogCreateView.as_view(), name='reception_visitorlog_new'),
    path('visitorlogs/<int:pk>/edit/', VisitorLogUpdateView.as_view(), name='reception_visitorlog_edit'),
    path('visitorlogs/<int:pk>/delete/', VisitorLogDeleteView.as_view(), name='reception_visitorlog_delete'),
]
