# Generated by Django 5.1.6 on 2025-02-14 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0006_remove_workout_days_of_week_remove_workout_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='day_of_week',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10),
        ),
        migrations.AlterField(
            model_name='workout',
            name='week_number',
            field=models.PositiveIntegerField(),
        ),
    ]
