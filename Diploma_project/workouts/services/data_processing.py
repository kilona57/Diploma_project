from django.db.models import F
import json

from users.models import CustomUser, UserProfile
from workouts.models import Exercise


def get_user_data(request):
    user_id = CustomUser.objects.get(email=request.user.email).id
    user_data = UserProfile.objects.filter(user=user_id).annotate(
        gender=F('gender__name'),
        activity_type=F('activity_type__name'),
        type_food=F('type_food__name'),
        main_goal=F('main_goal__name'),
        additional_goal=F('additional_goal__name')
    ).values(
        'gender',
        'height',
        'weight',
        'desired_weight',
        'activity_type',
        'type_food',
        'main_goal',
        'additional_goal'
    )[0]
    return user_id, user_data


def get_exercises_list():
    exercises_list = Exercise.objects.values_list('name', flat=True)
    return exercises_list


def process_ai_response(ai_response):
    json_str = ai_response.choices[0].message.content.strip('```json\n').strip('```')
    data = json.loads(json_str)
    return data


def add_data_to_the_db(user, exercise_data):

