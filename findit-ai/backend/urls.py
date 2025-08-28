# backend/urls.py (The main urls.py)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This now correctly points to the urls.py inside your 'api' app
    path('api/', include('api.urls')),
    path('accounts/', include('allauth.urls')), # Add this line
]