from django.urls import path
from .views import (
    CheckAuthView,
    ClaimCreateView,
    ClaimDetailView,
    FoundItemDetail,
    FoundItemListCreate,
    LostItemDetail,
    MyClaimsList,
    MyFoundItemsList,
    TestimonialCreateView,
    ApprovedTestimonialListView,
    SuccessStoryListView,
    PlatformStatsView,
    MyLostItemsView,
    AIMatchesShowcaseView,
    ConfirmExchangeView, # <-- 1. Import the new view
)

urlpatterns = [
    # Lost Item URLs
    path('my-lost-items/', MyLostItemsView.as_view(), name='my-lost-items'),
    path('lost-items/<int:pk>/', LostItemDetail.as_view(), name='lost-item-detail'),
    
    # Found Item URLs
    path('found-items/', FoundItemListCreate.as_view(), name='found-item-list-create'),
    path('found-items/<int:pk>/', FoundItemDetail.as_view(), name='found-item-detail'),
    path('my-found-items/', MyFoundItemsList.as_view(), name='my-found-items'),

    # Claim URLs
    path('claims/', ClaimCreateView.as_view(), name='claim-create'),
    path('claims/<int:pk>/', ClaimDetailView.as_view(), name='claim-detail'),
    path('my-claims/', MyClaimsList.as_view(), name='my-claims-list'),
    
    # --- 2. ADD THIS NEW URL FOR THE QR CODE SCAN ---
    path('claims/confirm-exchange/', ConfirmExchangeView.as_view(), name='claim-confirm-exchange'),

    # Testimonial URLs
    path('testimonials/submit/', TestimonialCreateView.as_view(), name='testimonial-create'),
    path('testimonials/', ApprovedTestimonialListView.as_view(), name='testimonial-list'),

    # Public & Auth URLs
    path('check-auth/', CheckAuthView.as_view(), name='check-auth'),
    path('success-stories/', SuccessStoryListView.as_view(), name='success-stories'),
    path('ai-matches-showcase/', AIMatchesShowcaseView.as_view(), name='ai-matches-showcase'),
    path('platform-stats/', PlatformStatsView.as_view(), name='platform-stats'),
]
