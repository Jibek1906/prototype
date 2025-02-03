from datetime import timedelta, date

def calculate_macros(food_logs):
    """Подсчет макронутриентов на основе записей о питании."""
    macros = {"protein": 0, "fats": 0, "carbs": 0, "calories": 0}
    for log in food_logs:
        macros["protein"] += log.food_item.protein * log.quantity / 100
        macros["fats"] += log.food_item.fats * log.quantity / 100
        macros["carbs"] += log.food_item.carbs * log.quantity / 100
        macros["calories"] += log.total_calories()
    return macros

def suggest_activity(user, food_logs, workout_logs):
    """
    Рекомендации на основе калорий, макронутриентов и тренировок.
    """
    macros = calculate_macros(food_logs)
    total_calories = macros["calories"]

    weekly_calories = sum([log.total_calories() for log in food_logs])
    weekly_workouts = sum([log.duration for log in workout_logs])

    daily_limit = 2000 if user.goal == 'lose-weight' else 2500

    recommendations = []

    if total_calories > daily_limit:
        recommendations.append(
            f"You consumed {total_calories - daily_limit} extra calories today. Add 30 minutes of cardio."
        )
    elif total_calories < daily_limit - 500:
        recommendations.append(
            f"You are under-eating by {daily_limit - total_calories} calories. Increase your intake."
        )

    protein_percentage = (macros["protein"] * 4) / total_calories * 100
    if protein_percentage < 20:
        recommendations.append("Increase your protein intake for better muscle recovery.")

    if weekly_workouts > 10 * 60:
        recommendations.append("You are overtraining. Take a rest day or reduce workout intensity.")

    if not recommendations:
        recommendations.append("Great job! Keep maintaining your current routine.")

    return {
        "macros": macros,
        "recommendations": recommendations,
        "weekly_calories": weekly_calories,
        "weekly_workouts": weekly_workouts
    }