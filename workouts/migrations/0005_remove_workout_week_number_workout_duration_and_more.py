# Generated by Django 5.1.6 on 2025-02-14 18:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0004_remove_workout_day_of_week_workout_days_of_week_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='week_number',
        ),
        migrations.AddField(
            model_name='workout',
            name='duration',
            field=models.IntegerField(default=10, help_text='Duration in minutes'),
        ),
        migrations.AddField(
            model_name='workout',
            name='workout_type',
            field=models.CharField(choices=[('bodyweight', 'Bodyweight'), ('strength', 'Strength'), ('cardio', 'Cardio'), ('yoga', 'Yoga'), ('pilates', 'Pilates'), ('stretching', 'Stretching'), ('hiit', 'HIIT'), ('endurance', 'Endurance'), ('core', 'Core'), ('balance', 'Balance'), ('flexibility', 'Flexibility'), ('rehab', 'Rehabilitation'), ('low_intensity', 'Low Intensity'), ('circuit', 'Circuit Training'), ('stretching_recovery', 'Stretching & Recovery'), ('weight_loss', 'Weight Loss'), ('muscle_gain', 'Muscle Gain'), ('yoga', 'Yoga')], default='yoga', max_length=50),
        ),
        migrations.AlterField(
            model_name='workout',
            name='goal',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='workout',
            name='max_weight',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='workout',
            name='min_weight',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='workout',
            name='repeat_every_n_weeks',
            field=models.IntegerField(default=1, help_text='Repeat every N weeks'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='training_level',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='UserWorkoutSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_date', models.DateField()),
                ('completed', models.BooleanField(default=False)),
                ('repeat_interval', models.IntegerField(default=7, help_text='Recurrence interval in days')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workouts.workout')),
            ],
        ),
    ]
