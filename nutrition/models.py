# from django.db import models
# from users.models import UserDetails  # Импортируем модель UserDetails из приложения users

# class CaloricIntake(models.Model):
#     user = models.OneToOneField(UserDetails, on_delete=models.CASCADE)
#     daily_calories = models.IntegerField()

#     def calculate_calories(self):
#         weight = self.user.weight
#         height = self.user.height
#         training_level = self.user.training_level
#         goal = self.user.goal

#         # Пример расчёта калорий (можно адаптировать с использованием более сложной формулы)
#         base_calories = 10 * weight + 6.25 * height - 5 * 30 + 5  # Основная формула для мужчин (для возраста 30)
#         if training_level == 'beginner':
#             base_calories *= 1.2
#         elif training_level == 'intermediate':
#             base_calories *= 1.375
#         elif training_level == 'advanced':
#             base_calories *= 1.55

#         if goal == 'lose-weight':
#             base_calories -= 500  # Дефицит калорий для похудения
#         elif goal == 'gain-muscle':
#             base_calories += 500  # Избыток калорий для набора массы

#         self.daily_calories = base_calories
#         self.save()

#     def __str__(self):
#         return f"{self.user.user.username} - {self.daily_calories} kcal/day"