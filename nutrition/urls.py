from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_food, name='log_food'),
]