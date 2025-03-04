from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserProfileForm, LoginForm
from .models import UserProfile


def main_page(request):
    return render(request, 'main_page.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("Пользователь аутентифицирован:", user.email)  # Логирование
            return redirect('edit_profile')  # Перенаправление после успешной регистрации
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    print('error', error)
            return render(request, 'main_page.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'registration_page.html', {'form': form})


@login_required
def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('register')
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            # form.save()
            user_profile = form.save(commit=False)
            user_profile.user = request.user  # Связываем профиль с пользователем
            user_profile.save()
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    print('error', error)
            return render(request, 'profile.html', {'form': form})
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    print('error', error)
            return render(request, 'main_page.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login_page.html', {'form': form})


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile.html', {'form': form, 'profile': user_profile})