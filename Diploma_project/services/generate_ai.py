import json

from openai import OpenAI
from DiplomaProject.settings import AI_TOKEN
from services.example_answer import example_answer_workout


def ai_generating_training(user_data, exercises_list):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=AI_TOKEN,
    )
    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[
            {
              "role": "user",
              "content": f"""
                            Данные пользователя:
                            - Пол: {user_data['gender']}
                            - Рост: {user_data['height']}
                            - Вес: {user_data['weight']}
                            - Желаемый вес: {user_data['desired_weight']}
                            - Уровень активности: {user_data['activity_type']}
                            - Тип питания: {user_data['type_food']}
                            - Основная цель: {user_data['main_goal']}
                            - Дополнительная цель: {user_data['additional_goal']}

                            Список доступных упражнений:
                            {', '.join(exercises_list)}

                            Задача:
                            Создай персональный план тренировок на основе предоставленных данных.
                            Учти уровень активности, цели и предпочтения пользователя.
                            
                            Ответ должен быть сформирован в виде json по вот такому вот примеру:
                                {json.dumps(example_answer_workout, ensure_ascii=False, indent=4)}
                            Важно что бы твой ответ полностью совпадал с моим примером что бы я мог его 
                            обработать в автоматическом режиме
                            В тех упражнениях в которых не повторения а время указывай "повторения": (количестов секунд 
                            в числовом формате)
                            
                            Ответ должен содержать только план тереновок который соответсвует примеру
                            убери из ответа рассуждения
                            
                            """
            }
          ]
                                                )
    return completion
