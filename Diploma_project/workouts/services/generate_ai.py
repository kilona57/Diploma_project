from openai import OpenAI
from DiplomaProject.settings import AI_TOKEN

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=AI_TOKEN,
)


user_data = {'gender': 'мужской',
             'height': '180',
             'weight': '95',
             'goal': 'похудеть',
             'desired weight': '75',
             'additional goals': 'проработка верхней части туловища',
             }

# model_ai = "deepseek/deepseek-chat",
messages_ai = [
    {
      "role": "user",
      "content": f"Составь программу тренеровок по переданным данным {user_data}, ответ сформируй ввиде json",
    }
  ]

# completion = client.chat.completions.create(
#   model="deepseek/deepseek-chat",
#   messages=messages_ai
# )
# print(completion.choices[0].message.content)


def ai_generating_training(data):
    completion = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {
              "role": "user",
              "content": f"Составь программу тренеровок по переданным данным {data}, ответ сформируй ввиде json",
            }
          ]
                                                )
    return completion


print(generating_training(user_data))