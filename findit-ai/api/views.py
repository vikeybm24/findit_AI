from rest_framework import generics, status, serializers, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import CustomUser, LostItem, FoundItem, Claim, Testimonial
from .serializers import (
    LostItemSerializer, 
    FoundItemSerializer, 
    ClaimSerializer, 
    ClaimDetailSerializer,
    TestimonialSerializer
)
from .permissions import IsOwner, IsFinderOrClaimant

# --- Lost Item Views ---
class MyLostItemsView(generics.ListCreateAPIView):
    serializer_class = LostItemSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return LostItem.objects.filter(user=self.request.user).order_by('-created_at')
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LostItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LostItem.objects.all()
    serializer_class = LostItemSerializer
    permission_classes = [IsAuthenticated, IsOwner]

# --- Found Item Views ---
class FoundItemListCreate(generics.ListCreateAPIView):
    queryset = FoundItem.objects.filter(status='available')
    serializer_class = FoundItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['item_name', 'description', 'location_found']
    def perform_create(self, serializer):
        serializer.save(finder=self.request.user)

class FoundItemDetail(generics.RetrieveAPIView):
    queryset = FoundItem.objects.all()
    serializer_class = FoundItemSerializer

class MyFoundItemsList(generics.ListAPIView):
    serializer_class = FoundItemSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return FoundItem.objects.filter(finder=self.request.user).order_by('-created_at')

# --- Claim Views ---
class ClaimCreateView(generics.CreateAPIView):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        found_item = serializer.validated_data.get('found_item')
        existing_active_claim = Claim.objects.filter(found_item=found_item, claimant=request.user).exclude(status='rejected').first()
        if existing_active_claim:
            return Response({"detail": "You have already placed an active claim on this item."}, status=status.HTTP_400_BAD_REQUEST)
        existing_rejected_claim = Claim.objects.filter(found_item=found_item, claimant=request.user, status='rejected').first()
        if existing_rejected_claim:
            existing_rejected_claim.status = 'pending'
            existing_rejected_claim.save()
            found_item.status = 'claimed'
            found_item.save()
            return Response(self.get_serializer(existing_rejected_claim).data, status=status.HTTP_200_OK)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        found_item = serializer.validated_data.get('found_item')
        if found_item.status != 'available':
            raise serializers.ValidationError("This item is no longer available for claims.")
        claim = serializer.save(claimant=self.request.user)
        found_item.status = 'claimed'
        found_item.save()

class ClaimDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Claim.objects.all()
    serializer_class = ClaimDetailSerializer
    permission_classes = [IsAuthenticated, IsFinderOrClaimant]
    def perform_update(self, serializer):
        instance = self.get_object()
        new_status = serializer.validated_data.get('status')
        if instance.status == 'match_found' and new_status == 'pending':
            instance = serializer.save(creation_method='ai_suggestion')
        else:
            instance = serializer.save()
        if instance.status == 'accepted':
            instance.found_item.status = 'claimed' 
            instance.found_item.save()
        if instance.status == 'resolved':
            instance.found_item.status = 'reunited'
            instance.found_item.save()
            if instance.lost_item:
                instance.lost_item.status = 'reunited'
                instance.lost_item.save()
        if instance.status == 'rejected':
            instance.found_item.status = 'available'
            instance.found_item.save()

class MyClaimsList(generics.ListAPIView):
    serializer_class = ClaimDetailSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Claim.objects.filter(claimant=self.request.user).order_by('-created_at')

class ConfirmExchangeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if not token:
            return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            claim = Claim.objects.get(exchange_token=token)
        except Claim.DoesNotExist:
            return Response({"error": "Invalid token."}, status=status.HTTP_404_NOT_FOUND)
        if request.user != claim.claimant:
            return Response({"error": "You are not authorized to confirm this exchange."}, status=status.HTTP_403_FORBIDDEN)
        if claim.status != 'accepted':
            return Response({"error": f"This claim cannot be resolved. Its status is '{claim.status}'."}, status=status.HTTP_400_BAD_REQUEST)
        claim.status = 'resolved'
        claim.save()
        claim.found_item.status = 'reunited'
        claim.found_item.save()
        if claim.lost_item:
            claim.lost_item.status = 'reunited'
            claim.lost_item.save()
        return Response({"success": "Exchange confirmed and claim resolved."}, status=status.HTTP_200_OK)

class TestimonialCreateView(generics.CreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        claim = serializer.validated_data.get('claim')
        if claim.claimant != self.request.user:
            raise serializers.ValidationError("You can only review claims you made.")
        serializer.save(user=self.request.user)

class ApprovedTestimonialListView(generics.ListAPIView):
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        return Testimonial.objects.filter(is_approved=True).order_by('-created_at')

class SuccessStoryListView(generics.ListAPIView):
    queryset = FoundItem.objects.filter(status='reunited').order_by('-created_at')
    serializer_class = FoundItemSerializer
    permission_classes = [AllowAny]

class AIMatchesShowcaseView(generics.ListAPIView):
    serializer_class = ClaimDetailSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        return Claim.objects.filter(creation_method='ai_suggestion').exclude(status='rejected').order_by('-created_at')

class PlatformStatsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        lost_items_count = LostItem.objects.count()
        found_items_count = FoundItem.objects.count()
        matches_made_count = Claim.objects.filter(creation_method='ai_suggestion').count()
        reunited_count = Claim.objects.filter(status='resolved').count()
        data = {"counts": {"lost_items": lost_items_count, "found_items": found_items_count, "matches_made": matches_made_count, "reunited": reunited_count}}
        return Response(data)

# --- THIS IS THE CORRECTED VIEW ---
class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        # This view now correctly returns the user's ID
        return Response({
            'isAuthenticated': True, 
            'email': request.user.email, 
            'username': request.user.username, 
            'id': request.user.id
        })