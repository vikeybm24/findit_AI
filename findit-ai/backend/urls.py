# File: backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Add this import
from django.conf.urls.static import static # Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]

# Add this line at the very end of the file
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)