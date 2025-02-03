from django.contrib import admin
from .models import Workout

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'day_of_week', 'week_number', 'goal', 'training_level')
    list_filter = ('day_of_week', 'week_number', 'goal', 'training_level')
    search_fields = ('title', 'description')