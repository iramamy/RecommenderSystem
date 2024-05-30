from django.contrib import admin
from .models import UserReview


class UserReviewAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'movieId',
        'rating',
        'updated_at',
    ]

    list_display_links = [
        'user',
        'movieId',
    ]

admin.site.register(UserReview, UserReviewAdmin)
