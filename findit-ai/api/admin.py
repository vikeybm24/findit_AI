# File: api/admin.py

from django.contrib import admin
from .models import CustomUser, LostItem, FoundItem, Claim, Testimonial

# This is a custom admin view for the Testimonial model
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    list_editable = ('is_approved',) # Allows you to edit directly from the list view
    search_fields = ('user__username', 'comment')
    list_per_page = 20

# Register your models here
admin.site.register(CustomUser)
admin.site.register(LostItem)
admin.site.register(FoundItem)
admin.site.register(Claim)
# We now register Testimonial with its custom admin view
admin.site.register(Testimonial, TestimonialAdmin)