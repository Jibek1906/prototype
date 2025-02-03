from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Workout
from users.models import UserDetails
from django.http import JsonResponse
from datetime import datetime

@login_required
def workouts_view(request):
    try:
        user_details = UserDetails.objects.get(user=request.user)
    except UserDetails.DoesNotExist:
        return render(request, 'workouts.html', {'error': 'User details not found'})

    today = request.GET.get('date', None)  

    if today:
        workouts = Workout.objects.filter(
            day_of_week=today,
            goal=user_details.goal,
            training_level=user_details.training_level,
            min_weight__lte=user_details.weight,
            max_weight__gte=user_details.weight
        )
    else:
        workouts = Workout.objects.none()

    return render(request, 'workouts.html', {
        'user_details': user_details,
        'workouts': workouts,
        'today': today
    })

@login_required
def workouts_api(request):
    try:
        user_details = UserDetails.objects.get(user=request.user)
    except UserDetails.DoesNotExist:
        return JsonResponse({'error': 'User details not found'}, status=400)

    today_str = request.GET.get('date', None)

    if not today_str:
        return JsonResponse({'error': 'No date provided'}, status=400)

    # Преобразуем YYYY-MM-DD в день недели (Monday, Tuesday и т.д.)
    try:
        today_date = datetime.strptime(today_str, "%Y-%m-%d")
        day_of_week = today_date.strftime("%A")  # Monday, Tuesday, etc.
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    workouts = Workout.objects.filter(
        day_of_week=day_of_week,  # Теперь фильтруем по 'Monday', 'Tuesday' и т.д.
        goal=user_details.goal,
        training_level=user_details.training_level,
        min_weight__lte=user_details.weight,
        max_weight__gte=user_details.weight
    ).values('title', 'description', 'video_url')

    return JsonResponse({'workouts': list(workouts)}, safe=False)