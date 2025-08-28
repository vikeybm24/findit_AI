# File path: api/urls.py

from django.urls import path
from .views import LostItemListCreate, FoundItemListCreate

urlpatterns = [
    path('lost-items/', LostItemListCreate.as_view(), name='lost-item-list-create'),
    path('found-items/', FoundItemListCreate.as_view(), name='found-item-list-create'),
]