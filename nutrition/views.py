from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .ai_module import suggest_activity
from workouts.models import Workout
from .models import FoodItem

def log_food(request):
    if request.method == 'POST':
        food_item_id = request.POST.get('food_item_id')
        quantity = int(request.POST.get('quantity'))
        user = request.user.userdetails
        food_item = FoodItem.objects.get(id=food_item_id)
        log = UserFoodLog(user=user, food_item=food_item, quantity=quantity)
        log.save()

        today = date.today()
        last_week = today - timedelta(days=7)
        food_logs = UserFoodLog.objects.filter(user=user, date__gte=last_week)
        workout_logs = WorkoutLog.objects.filter(user=user, date__gte=last_week)

        analytics = suggest_activity(user, food_logs, workout_logs)

        return render(request, 'nutrition.html', {
            'analytics': analytics,
            'food_items': FoodItem.objects.all()
        })

    food_items = FoodItem.objects.all()
    return render(request, 'nutrition.html', {'food_items': food_items})