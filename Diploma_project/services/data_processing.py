import json

from users.models import CustomUser, UserProfile
from workouts.models import Exercise, TypeOfWorkout, DayNumber, Training, TrainingSchedule


def get_user_data(request):
    user_id = CustomUser.objects.get(email=request.user.email).id
    user_data = UserProfile.objects.filter(user=user_id).values(
        'gender',
        'activity_type',
        'type_food',
        'main_goal',
        'additional_goal',
        'height',
        'weight',
        'desired_weight',
    )[0]
    return user_id, user_data


def get_exercises_list():
    exercises_list = Exercise.objects.values_list('name', flat=True)
    return exercises_list


def process_ai_response(ai_response):
    json_str = ai_response.choices[0].message.content.strip('```json\n').strip('```')
    data = json.loads(json_str)
    return data


def add_ai_training_data_to_the_db(user_id, exercise_data):
    # создаем новую тренировку
    new_training = Training.objects.create(
        user=CustomUser.objects.get(id=user_id),
        type_of_workout=TypeOfWorkout.objects.get(name='Сгенерированная')
    )
    # проверяем валидность данных
    for day, training in exercise_data.items():
        train = training['тренировка']
        for i in train:
            if Exercise.objects.filter(name=i['упражнение']).exists():
                repeat = i['повторения']
                approaches = i['подходы']
    # записываем расписание тренировки в базу
    for day, training in exercise_data.items():
        train = training['тренировка']
        for i in train:
            if Exercise.objects.filter(name=i['упражнение']).exists():
                TrainingSchedule.objects.create(
                    training=new_training,
                    day_number=DayNumber.objects.get(name=day),
                    exercise=Exercise.objects.filter(name=i['упражнение']).first(),
                    repeat=i['повторения'],
                    approaches=i['подходы']
                )
