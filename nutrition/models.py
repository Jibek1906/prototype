from django.db import models

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField(default=0)
    protein = models.FloatField(default=0)
    fats = models.FloatField(default=0)
    carbs = models.FloatField(default=0)

    def __str__(self):
        return self.name

class UserFoodLog(models.Model):
    user = models.ForeignKey('users.UserDetails', on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()

    def total_calories(self):
        return self.food_item.calories * self.quantity / 100
