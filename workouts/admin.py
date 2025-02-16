from django.contrib import admin
from .models import Workout

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'day_of_week', 'week_number', 'goal', 'training_level', 'repeat_interval')
    list_filter = ('day_of_week', 'week_number', 'goal', 'training_level', 'repeat_interval')
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'video_url')
        }),
        ('Filters', {
            'fields': ('goal', 'training_level', 'min_weight', 'max_weight')
        }),
        ('Schedule', {
            'fields': ('day_of_week', 'week_number', 'repeat_interval')
        }),
    )
