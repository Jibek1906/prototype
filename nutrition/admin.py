from django.contrib import admin
from . import models

admin.site.register(models.FoodItem)
admin.site.register(models.UserFoodLog)
