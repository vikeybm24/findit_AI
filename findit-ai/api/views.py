# File path: api/views.py

from rest_framework import generics
from .models import LostItem, FoundItem
from .serializers import LostItemSerializer, FoundItemSerializer

# This view handles listing all lost items and creating a new one
class LostItemListCreate(generics.ListCreateAPIView):
    queryset = LostItem.objects.all()
    serializer_class = LostItemSerializer

# This view handles listing all found items and creating a new one
class FoundItemListCreate(generics.ListCreateAPIView):
    queryset = FoundItem.objects.all()
    serializer_class = FoundItemSerializer