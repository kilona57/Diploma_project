from django.shortcuts import render

from workouts.services.data_processing import get_user_data, get_exercises_list,\
    process_ai_response, add_ai_training_data_to_the_db
from workouts.services.generate_ai import ai_generating_training


def exercises(request):
    return render(request, 'edit_workout.html')


def generate_training(request):
    # получаем айди пользователя (user_id) и
    # данные профиля пользователя (user_data)
    user_id, user_data = get_user_data(request=request)
    # получаем список доступных упражнений
    exercises_list = get_exercises_list()
    # генерируем тренеровку для пользователя на основе его профиля
    generated_training = ai_generating_training(user_data, exercises_list)
    # обрабатываем ответ ИИ и приветом его к словарю
    ai_data_response = process_ai_response(generated_training)
    # записываем полученные данные в БД
    add_ai_training_data_to_the_db(user_id, ai_data_response)
    pass
