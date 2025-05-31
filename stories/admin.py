from django.contrib import admin
from .models import DonationStory


@admin.register(DonationStory)
class DonationStoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    ordering = ('-created_at',)
