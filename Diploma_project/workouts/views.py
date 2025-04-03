import time
from django.shortcuts import render

from services.data_processing import get_user_data, get_exercises_list,\
    process_ai_response, add_ai_training_data_to_the_db
from services.generate_ai import ai_generating_training

MAX_RETRIES = 5  # Максимальное количество попыток
RETRY_DELAY = 2   # Задержка между попытками (в секундах)


def exercises(request):
    # отображение страницы с выбором тренеровки (наверное) доработаь
    return render(request, 'edit_workout.html')


def generate_training(request):
    retry_count = 0
    # получаем айди пользователя (user_id) и
    # данные профиля пользователя (user_data)
    user_id, user_data = get_user_data(request=request)
    # получаем список доступных упражнений
    exercises_list = get_exercises_list()
    # в цикле получаем ответ от ИИ и пытаемся его обработать с записью в бд
    # иногда ИИ отвечает не привильно и обработчик ответа выдает ошибку
    while retry_count < MAX_RETRIES:
        try:
            # генерируем тренеровку для пользователя на основе его профиля
            generated_training = ai_generating_training(user_data, exercises_list)
            # обрабатываем ответ ИИ и приветом его к словарю
            ai_data_response = process_ai_response(generated_training)
            # записываем полученные данные в БД
            add_ai_training_data_to_the_db(user_id, ai_data_response)
            # вернуть пользователя куда нибудь после нажания на кнопку "сгенерировать"
            return
        except Exception as e:
            print(f"Попытка {retry_count + 1}: Критическая ошибка - {e}")
            retry_count += 1
            time.sleep(RETRY_DELAY)
    raise Exception(f"Не удалось получить валидный ответ после {MAX_RETRIES} попыток")
