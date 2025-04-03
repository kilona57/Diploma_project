from django.core.management import call_command
from django.test import TestCase, Client
from users.models import CustomUser, UserProfile, Gender,\
    ActivityType, TypeFood, MainGoal
from workouts.views import generate_training
from workouts.models import TrainingSchedule


class AIGenerateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Загружаем фикстуры и создаем общие данные для всех тестов"""
        call_command('loaddata', 'activity_type_fixture.json')
        call_command('loaddata', 'additional_goal_fixture.json')
        call_command('loaddata', 'gender_fixture.json')
        call_command('loaddata', 'main_goal_fixture.json')
        call_command('loaddata', 'type_food_fixture.json')
        call_command('loaddata', 'difficulty_fixture.json')
        call_command('loaddata', 'muscle_group_fixture.json')
        call_command('loaddata', 'equipment_fixture.json')
        call_command('loaddata', 'exercises_fixture.json')
        call_command('loaddata', 'exercise_gif_fixture.json')
        call_command('loaddata', 'day_fixture.json')
        call_command('loaddata', 'type_training_fixture.json')

    def setUp(self) -> None:
        # создаем клиент
        self.client = Client()
        # создаем тестового пользователя
        self.user = CustomUser.objects.create(
            first_name='TestUser',
            email='TestUser@mail.ru',
            password='123testuser123',
        )
        # заполняем профиль пользователя данными
        self.userprofile = UserProfile.objects.create(
            user=self.user,
            gender=Gender.objects.get(id=1),
            height=180,
            weight=90,
            desired_weight=75,
            activity_type=ActivityType.objects.get(id=2),
            type_food=TypeFood.objects.get(id=2),
            main_goal=MainGoal.objects.get(id=1),
        )

    def test_user_profile_creation(self):
        """Проверяем, что профиль создан правильно"""
        self.assertEqual(self.userprofile.user.first_name, 'TestUser')
        self.assertEqual(self.userprofile.height, 180)
        self.assertEqual(self.userprofile.activity_type,
                         ActivityType.objects.get(id=2))

    def test_ai_generation(self):
        """Проверяем работу генератора тренировок"""
        # Логиним пользователя
        self.client.force_login(self.user)
        # создаем request через клиент
        request = self.client.request().wsgi_request
        # создаем расписание тренировок
        generate_training(request)
        # получаем расписание тренировок и выводим в консоль
        training_schedule = TrainingSchedule.objects.all()

        for i in training_schedule:
            print(f'{i.id},'
                  f'{i.training},'
                  f'{i.day_number},'
                  f'{i.exercise},'
                  f'{i.repeat},'
                  f'{i.approaches} ')
