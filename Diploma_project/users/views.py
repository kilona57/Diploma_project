from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserProfileForm, BodyParametersForm, NutritionGoalsForm
from .models import UserProfile, BodyParameters, NutritionGoals

from .forms import EmailAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


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


User = get_user_model()


def user_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # Получаем email из поля username
            password = form.cleaned_data.get('password')

            # Ищем пользователя по email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            # Аутентифицируем пользователя
            if user is not None and user.check_password(password):
                login(request, user)
                return redirect('profile')  # Перенаправляем на главную страницу
            else:
                error_message = "Неправильный email или пароль."  # Сообщение об ошибке
        else:
            error_message = "Пожалуйста, исправьте ошибки в форме."  # Ошибки валидации формы
    else:
        form = AuthenticationForm()

    return render(request, 'login_page.html', {'form': form})


# @login_required
# def profile(request):
#     # Получаем или создаем профиль пользователя
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)
#
#     # Получаем или создаем параметры тела пользователя
#     body_parameters, created = BodyParameters.objects.get_or_create(user=request.user)
#
#     if request.method == 'POST':
#         # Определяем, какая форма была отправлена
#         if 'profile_form' in request.POST:
#             profile_form = UserProfileForm(request.POST, instance=user_profile)
#             if profile_form.is_valid():
#                 profile_form.save()
#                 return redirect('profile')
#         elif 'body_parameters_form' in request.POST:
#             body_parameters_form = BodyParametersForm(request.POST, instance=body_parameters)
#             if body_parameters_form.is_valid():
#                 body_parameters_form.save()
#                 return redirect('profile')
#     else:
#         profile_form = UserProfileForm(instance=user_profile)
#         body_parameters_form = BodyParametersForm(instance=body_parameters)
#
#     return render(request, 'profile.html', {
#         'profile_form': profile_form,
#         'body_parameters_form': body_parameters_form,
#         'profile': user_profile,
#         'body_parameters': body_parameters,
#     })
@login_required
def profile(request):
    # Получаем или создаем профиль пользователя
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Получаем или создаем параметры тела пользователя
    body_parameters, created = BodyParameters.objects.get_or_create(user=request.user)

    # Получаем или создаем цели по КБЖУ
    nutrition_goals, created = NutritionGoals.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Определяем, какая форма была отправлена
        if 'profile_form' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=user_profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')
        elif 'body_parameters_form' in request.POST:
            body_parameters_form = BodyParametersForm(request.POST, instance=body_parameters)
            if body_parameters_form.is_valid():
                body_parameters_form.save()
                return redirect('profile')
        elif 'nutrition_goals_form' in request.POST:  # Обработка формы КБЖУ
            nutrition_goals_form = NutritionGoalsForm(request.POST, instance=nutrition_goals)
            if nutrition_goals_form.is_valid():
                nutrition_goals_form.save()
                return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)
        body_parameters_form = BodyParametersForm(instance=body_parameters)
        nutrition_goals_form = NutritionGoalsForm(instance=nutrition_goals)  # Форма КБЖУ

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'body_parameters_form': body_parameters_form,
        'nutrition_goals_form': nutrition_goals_form,  # Передаем форму КБЖУ в контекст
        'profile': user_profile,
        'body_parameters': body_parameters,
        'nutrition_goals': nutrition_goals,  # Передаем объект КБЖУ в контекст
    })


def logout_view(request):
    logout(request)
    return redirect('main_page')  # Перенаправление на гравную страницу
#
#
# # @login_required
# # def update_body_parameters(request):
# #     try:
# #         body_parameters = request.user.body_parameters
# #     except BodyParameters.DoesNotExist:
# #         body_parameters = BodyParameters(user=request.user)
# #
# #     if request.method == 'POST':
# #         form = BodyParametersForm(request.POST, instance=body_parameters)
# #         if form.is_valid():
# #             form.save()
# #             return redirect('profile')  # Перенаправляем обратно на страницу профиля
# #     else:
# #         form = BodyParametersForm(instance=body_parameters)
# #
# #     return render(request, 'profile.html', {'body_parameters_form': form})
#
# @login_required
# def update_body_parameters(request):
#     try:
#         body_parameters = request.user.body_parameters
#     except BodyParameters.DoesNotExist:
#         body_parameters = BodyParameters(user=request.user)
#     print(body_parameters)
#     if request.method == 'POST':
#         print("Данные POST-запроса:", request.POST)  # Отладочное сообщение
#         form = BodyParametersForm(request.POST, instance=body_parameters)
#         if form.is_valid():
#             print("Форма валидна")  # Отладочное сообщение
#             weight = form.cleaned_data.get('weight')
#             print(f"Новый вес из формы: {weight}")  # Отладочное сообщение
#
#             user_profile = request.user.profile
#             print(f"Текущий вес в UserProfile до обновления: {user_profile.weight}")  # Отладочное сообщение
#             user_profile.weight = weight
#             user_profile.save()
#             print(f"Вес в UserProfile после обновления: {user_profile.weight}")  # Отладочное сообщение
#
#             form.save()
#             return redirect('profile')
#         else:
#             print("Форма не валидна")  # Отладочное сообщение
#             print(form.errors)  # Вывод ошибок формы
#     else:
#         initial_data = {'weight': request.user.profile.weight}
#         form = BodyParametersForm(instance=body_parameters, initial=initial_data)
#
#     return render(request, 'profile.html', {'body_parameters_form': form})
def update_body_parameters(request):
    try:
        body_parameters = request.user.body_parameters
    except BodyParameters.DoesNotExist:
        body_parameters = BodyParameters(user=request.user)

    if request.method == 'POST':
        print("Данные POST-запроса:", request.POST)  # Отладочное сообщение
        form = BodyParametersForm(request.POST, instance=body_parameters)
        if form.is_valid():
            print("Форма валидна")  # Отладочное сообщение

            # Обновляем вес в UserProfile
            weight = form.cleaned_data.get('weight')
            if weight is not None:
                user_profile = request.user.profile
                user_profile.weight = weight
                user_profile.save()

            # Обновляем желаемый вес в UserProfile
            desired_weight = form.cleaned_data.get('desired_weight')
            if desired_weight is not None:
                user_profile = request.user.profile
                user_profile.desired_weight = desired_weight
                user_profile.save()

            form.save()
            return redirect('profile')
        else:
            print("Форма не валидна")  # Отладочное сообщение
            print(form.errors)  # Вывод ошибок формы
    else:
        initial_data = {
            'weight': request.user.profile.weight,
            'desired_weight': request.user.profile.desired_weight,  # Добавляем начальное значение для желаемого веса
        }
        form = BodyParametersForm(instance=body_parameters, initial=initial_data)

    return render(request, 'profile.html', {'body_parameters_form': form})
@login_required
def update_nutrition_goals(request):
    user_profile = request.user.profile
    nutrition_goals, created = NutritionGoals.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = NutritionGoalsForm(request.POST, instance=nutrition_goals)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = NutritionGoalsForm(instance=nutrition_goals)

    return render(request, 'profile.html', {'nutrition_goals_form': form})