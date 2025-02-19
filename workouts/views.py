from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Workout  # ✅ Используем модель из models.py
from users.models import UserDetails
from datetime import datetime
from django.db.models import Q

@login_required
def workouts_view(request):
    try:
        user_details = UserDetails.objects.get(user=request.user)
    except UserDetails.DoesNotExist:
        return render(request, 'workouts.html', {'error': 'User details not found'})

    today_str = request.GET.get('date', None)

    if today_str:
        try:
            today_date = datetime.strptime(today_str, "%Y-%m-%d")
            day_of_week = today_date.strftime("%A")
            week_number = today_date.isocalendar()[1]
        except ValueError:
            return render(request, 'workouts.html', {'error': 'Invalid date format'})

        # Получение всех тренировок, соответствующих пользователю
        all_workouts = Workout.objects.filter(
            Q(goal=user_details.goal) &
            Q(training_level=user_details.training_level) &
            Q(min_weight__lte=user_details.weight) &
            Q(max_weight__gte=user_details.weight)
        )

        # Фильтрация по неделям и дням
        workouts = [
            workout for workout in all_workouts
            if week_number % workout.repeat_interval_weeks == 0 and day_of_week in workout.repeat_days
        ]
    else:
        workouts = Workout.objects.none()

    return render(request, 'workouts.html', {
        'workouts': workouts,
        'today': today_str
    })

@login_required
def workouts_api(request):
    try:
        user_details, _ = UserDetails.objects.get_or_create(
            user=request.user,
            defaults={
                'height': 170,
                'weight': 70,
                'goal': 'maintain',
                'training_level': 'beginner',
                'birth_date': '2000-01-01'
            }
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    today_str = request.GET.get('date', datetime.now().strftime("%Y-%m-%d"))

    try:
        today_date = datetime.strptime(today_str, "%Y-%m-%d")
        day_of_week = today_date.strftime("%A")
        week_number = today_date.isocalendar()[1]
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    # Получение всех тренировок, соответствующих пользователю
    all_workouts = Workout.objects.filter(
        Q(goal=user_details.goal) &
        Q(training_level=user_details.training_level) &
        Q(min_weight__lte=user_details.weight) &
        Q(max_weight__gte=user_details.weight)
    )

    # Фильтрация по неделям и дням
    filtered_workouts = [
        workout for workout in all_workouts
        if week_number % workout.repeat_interval_weeks == 0 and day_of_week in workout.repeat_days
    ]

    return JsonResponse({'workouts': [{
        'title': w.title,
        'description': w.description,
        'video_url': w.video_url,
        'video_file': w.video_file.url if w.video_file else None
    } for w in filtered_workouts]}, safe=False)
