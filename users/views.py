from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import UserDetailsForm
from django.contrib.auth.models import User
from .forms import LoginForm
from .models import UserDetails, WeightRecord
from .forms import CustomUserCreationForm

def main(request):
    return render(request, 'main.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserDetails.objects.create(
                user=user,
                height=170,
                weight=70,
                goal='maintain',
                training_level='beginner'
            )
            return redirect('user_details', user_id=user.id)  # Перенаправляем на страницу user_details
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)  # Используем email как username
            if user is not None:
                login(request, user)
                return redirect('personal_office', user_id=user.id)
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)

    try:
        user_details = UserDetails.objects.get(user=user)
    except UserDetails.DoesNotExist:
        user_details = UserDetails.objects.create(
            user=user,
            height=170,
            weight=70,
            goal='maintain',
            training_level='beginner'
        )

    form = UserDetailsForm(request.POST or None, instance=user_details)

    if form.is_valid():
        form.save()
        return redirect('login')  # Redirect to login after user details
    return render(request, 'user_details.html', {'form': form, 'user_details': user_details})

@login_required
def personal_office(request, user_id):
    user_details = get_object_or_404(UserDetails, user__id=user_id)
    weight_records = WeightRecord.objects.filter(user=user_details).order_by('date')

    labels = [record.date.strftime('%d.%m.%Y') for record in weight_records]
    weights = [record.weight for record in weight_records]

    context = {
        'user_details': user_details,
        'labels': labels,
        'weights': weights,
    }

    return render(request, 'personal_office.html', context)

@login_required
def update_user_details(request, user_id):
    user_details = get_object_or_404(UserDetails, user__id=user_id)
    if request.method == 'POST':
        new_weight = request.POST.get('weight')
        new_height = request.POST.get('height')
        new_goal = request.POST.get('goal')
        new_training_level = request.POST.get('training_level')
        new_avatar = request.FILES.get('avatar')

        user_details.height = new_height
        user_details.weight = new_weight
        user_details.goal = new_goal
        user_details.training_level = new_training_level

        if new_avatar:
            user_details.avatar = new_avatar

        user_details.save()

        WeightRecord.objects.create(
            user=user_details,
            weight=new_weight,
            date=timezone.now().date()
        )

        return redirect('personal_office', user_id=user_details.user.id)

    return render(request, 'users/personal_office.html', {'user_details': user_details})