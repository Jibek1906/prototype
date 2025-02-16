from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Workout
from users.models import UserDetails
from datetime import datetime
from django.db.models import F

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

        workouts = Workout.objects.filter(
            day_of_week=day_of_week,
            goal=user_details.goal,
            training_level=user_details.training_level,
            min_weight__lte=user_details.weight,
            max_weight__gte=user_details.weight
        ).filter(
            (week_number % F('repeat_interval')) == 0
        )

        print(f"User's goal: {user_details.goal}")
        print(f"User's training level: {user_details.training_level}")
        print(f"User's weight: {user_details.weight}")
        print(f"Day of week: {day_of_week}")
        print(f"Week number: {week_number}")
        print(f"Filtered workouts: {workouts}")

    else:
        workouts = Workout.objects.none()

    return render(request, 'workouts.html', {
        'workouts': workouts,
        'today': today_str
    })

@login_required
def workouts_api(request):
    try:
        user_details, created = UserDetails.objects.get_or_create(
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

    workouts = Workout.objects.filter(
        day_of_week=day_of_week,
        week_number=week_number,
        goal=user_details.goal,
        training_level=user_details.training_level,
        min_weight__lte=user_details.weight,
        max_weight__gte=user_details.weight
    ).filter(
        (week_number % F('repeat_interval')) == 0
    ).values('title', 'description', 'video_url')

    return JsonResponse({'workouts': list(workouts)}, safe=False)
