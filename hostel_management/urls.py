

from django.contrib import admin
from django.urls import path, include

from .admin_dashboard_view import AdminDashboardView
from .views import HomePageView, StaffLogoutView, AboutUsView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('students/', include('students.urls')),
    path('hostel-admin/', include('hostel_management.admin_urls')),
    path('reception/', include('hostel_management.reception_urls')),
    path('manage/', include('rooms.custom_urls')),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('logout/', StaffLogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
