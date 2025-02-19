from django import forms
from django.contrib import admin
from .models import Workout

# Форма для админки с выбором дней недели
class WorkoutAdminForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = '__all__'

    repeat_days = forms.MultipleChoiceField(
        choices=[
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday')
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Repeat Days"
    )

    def clean_repeat_days(self):
        # Преобразуем выбранные дни в список чисел
        return list(map(int, self.cleaned_data['repeat_days']))

# Админская модель для Workout
@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    form = WorkoutAdminForm  # Применяем нашу форму для админки
    list_display = ('title', 'goal', 'training_level', 'min_weight', 'max_weight', 'repeat_interval_weeks', 'repeat_days_display')
    list_filter = ('goal', 'training_level', 'repeat_interval_weeks')
    search_fields = ('title', 'description')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'video_url', 'video_file')
        }),
        ('Filters', {
            'fields': ('goal', 'training_level', 'min_weight', 'max_weight')
        }),
        ('Repeat Interval (Weeks)', {
            'fields': ('repeat_interval_weeks',)
        }),
        ('Repeat Days', {
            'fields': ('repeat_days',)
        }),
    )

    def repeat_days_display(self, obj):
        # Показываем дни недели в виде текста
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return ', '.join([days[day] for day in obj.repeat_days])
    repeat_days_display.short_description = 'Repeat Days'
