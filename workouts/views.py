from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Workout
from users.models import UserDetails
from datetime import datetime

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
            day_of_week = today_date.strftime("%A")  # Converts to Monday, Tuesday, etc.
            week_number = today_date.isocalendar()[1]  # Gets the week number
        except ValueError:
            return render(request, 'workouts.html', {'error': 'Invalid date format'})

        # Debugging logs
        print(f"User Goal: {user_details.goal}")
        print(f"User Training Level: {user_details.training_level}")
        print(f"User Weight: {user_details.weight}")
        print(f"Day of Week: {day_of_week}, Week Number: {week_number}")

        workouts = Workout.objects.filter(
            day_of_week=day_of_week,
            week_number=week_number,
            goal=user_details.goal,
            training_level=user_details.training_level,
            min_weight__lte=user_details.weight,
            max_weight__gte=user_details.weight
        )

        # Debugging log for filtered workouts
        print(f"Found {len(workouts)} workouts.")

    else:
        workouts = Workout.objects.none()

    return render(request, 'workouts.html', {
        'user_details': user_details,
        'workouts': workouts,
        'today': today_str
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

    try:
        today_date = datetime.strptime(today_str, "%Y-%m-%d")
        day_of_week = today_date.strftime("%A")  # Monday, Tuesday, etc.
        week_number = today_date.isocalendar()[1]  # Получаем номер недели
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    workouts = Workout.objects.filter(
        day_of_week=day_of_week,
        week_number=week_number,
        goal=user_details.goal,
        training_level=user_details.training_level,
        min_weight__lte=user_details.weight,
        max_weight__gte=user_details.weight
    ).values('title', 'description', 'video_url')

    return JsonResponse({'workouts': list(workouts)}, safe=False)
