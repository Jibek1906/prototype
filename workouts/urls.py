from django.urls import path
from .views import workouts_view, workouts_api

urlpatterns = [
    path('workouts/', workouts_view, name='workouts'),
    path('workouts/api/', workouts_api, name='workouts_api'),
]