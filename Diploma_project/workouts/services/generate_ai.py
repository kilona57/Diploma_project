import os
import django
from django.db.models import F

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DiplomaProject.settings')
django.setup()


from openai import OpenAI
from DiplomaProject.settings import AI_TOKEN
from workouts.services.data_processing import get_exercises_list
from users.models import UserProfile


def ai_generating_training(user_data, exercises_list):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=AI_TOKEN,
    )
    completion = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {
              "role": "user",
              "content": f"""
                            Данные пользователя:
                            - Пол: {user_data['gender_type']}
                            - Рост: {user_data['height']}
                            - Вес: {user_data['weight']}
                            - Желаемый вес: {user_data['desired_weight']}
                            - Уровень активности: {user_data['activity_name']}
                            - Тип питания: {user_data['type_food_name']}
                            - Основная цель: {user_data['main_goal_name']}
                            - Дополнительная цель: {user_data['additional_goal_name']}

                            Список доступных упражнений:
                            {', '.join(exercises_list)}

                            Задача:
                            Создай персональный план тренировок и план питания на основе предоставленных данных.
                            Учти уровень активности, цели и предпочтения пользователя.
                            
                            Ответ должен быть сформирован в виде json:
                                день 1: тренеровки
                                день 2: тренеровки
                                
                                питание:
                            """
            }
          ]
                                                )
    return completion


user = UserProfile.objects.filter(user=2).annotate(
        gender_type=F('gender__name'),
        activity_name=F('activity_type__name'),
        type_food_name=F('type_food__name'),
        main_goal_name=F('main_goal__name'),
        additional_goal_name=F('additional_goal__name')
    ).values(
        'gender_type',
        'height',
        'weight',
        'desired_weight',
        'activity_name',
        'type_food_name',
        'main_goal_name',
        'additional_goal_name'
    )[0]
exercises = get_exercises_list()
print(user)
training = ai_generating_training(user_data=user, exercises_list=exercises)
print('генерация окончена')



# messages_ai = [
#     {
#       "role": "user",
#       "content": f"Составь программу тренеровок по переданным данным {user_data}, ответ сформируй ввиде json",
#     }
#   ]


# user_data = {'gender': 'мужской',
#              'height': '180',
#              'weight': '95',
#              'goal': 'похудеть',
#              'desired weight': '75',
#              'additional goals': 'проработка верхней части туловища',
#              }

# model_ai = "deepseek/deepseek-chat",

# completion = client.chat.completions.create(
#   model="deepseek/deepseek-chat",
#   messages=messages_ai
# )
# print(completion.choices[0].message.content)


ChatCompletion(id='gen-1742360857-0kc9o6i3pIXXdMGc2Haw', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='```json\n{\n    "день 1": {\n        "тренировка": [\n            {"упражнение": "Классические отжимания", "подходы": 3, "повторения": 12},\n            {"упражнение": "Приседания с гантелями в руках", "подходы": 3, "повторения": 15},\n            {"упражнение": "Тяга гантели в наклоне", "подходы": 3, "повторения": 10},\n            {"упражнение": "Жим гантелей под положительным углом", "подходы": 3, "повторения": 12},\n            {"упражнение": "Ягодичный мостик", "подходы": 3, "повторения": 15},\n            {"упражнение": "Скручивания", "подходы": 3, "повторения": 20}\n        ]\n    },\n    "день 2": {\n        "тренировка": [\n            {"упражнение": "Выпады с гантелями", "подходы": 3, "повторения": 12},\n            {"упражнение": "Жим штанги лежа", "подходы": 3, "повторения": 10},\n            {"упражнение": "Подтягивания широким хватом", "подходы": 3, "повторения": 8},\n            {"упражнение": "Мертвая тяга с гантелями", "подходы": 3, "повторения": 12},\n            {"упражнение": "Косые скручивания", "подходы": 3, "повторения": 20},\n            {"упражнение": "Пловец (без участия ног)", "подходы": 3, "повторения": 15}\n        ]\n    },\n    "питание": {\n        "завтрак": "Овсянка с фруктами и орехами, вареное яйцо, чай без сахара",\n        "перекус": "Йогурт натуральный с ложкой меда",\n        "обед": "Куриная грудка на пару, гречка, салат из свежих овощей с оливковым маслом",\n        "перекус": "Творог с ягодами",\n        "ужин": "Запеченная рыба, тушеные овощи, зеленый чай",\n        "перед сном": "Кефир или ряженка"\n    }\n}\n```', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None), native_finish_reason='stop')], created=1742360857, model='deepseek/deepseek-chat', object='chat.completion', service_tier=None, system_fingerprint='', usage=CompletionUsage(completion_tokens=590, prompt_tokens=2928, total_tokens=3518, completion_tokens_details=None, prompt_tokens_details=None), provider='Novita')