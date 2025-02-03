from django.db import models
from users.models import UserDetails

class Workout(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField()
    goal = models.CharField(max_length=50, choices=UserDetails.goal_choices)
    training_level = models.CharField(max_length=50, choices=UserDetails.training_level_choices)
    min_weight = models.PositiveIntegerField(default=40)
    max_weight = models.PositiveIntegerField(default=50)
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')
    ])
    week_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} ({self.day_of_week}, Week {self.week_number})"