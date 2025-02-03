# calorie_service.py

class CalorieCalculator:
    @staticmethod
    def calculate_calories(weight, height, training_level, goal):
        """
        Рассчитывает дневную норму калорий на основе данных пользователя.
        """
        # Упрощенная формула BMR
        bmr = 10 * weight + 6.25 * height

        # Умножение на коэффициент активности
        if training_level == 'beginner':
            bmr *= 1.2
        elif training_level == 'intermediate':
            bmr *= 1.375
        elif training_level == 'advanced':
            bmr *= 1.55

        # Корректировка по цели
        if goal == 'lose-weight':
            bmr -= 500
        elif goal == 'gain-muscle':
            bmr += 500

        return int(bmr)

    @staticmethod
    def get_training_recommendation(calories_consumed, daily_calorie_goal):
        """
        Рекомендации по тренировкам, если превышена дневная норма калорий.
        """
        if calories_consumed > daily_calorie_goal:
            excess_calories = calories_consumed - daily_calorie_goal
            if excess_calories <= 300:
                return "Легкая тренировка: 30 минут ходьбы или йоги."
            elif excess_calories <= 600:
                return "Средняя тренировка: 45 минут бега или силовой тренировки."
            else:
                return "Интенсивная тренировка: 60 минут HIIT или кроссфита."
        else:
            return "Вы в пределах нормы. Тренировка не требуется."