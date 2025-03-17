import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DiplomaProject.settings')
django.setup()

os.system('python manage.py loaddata activity_type_fixture.json')
os.system('python manage.py loaddata additional_goal_fixture.json')
os.system('python manage.py loaddata gender_fixture.json')
os.system('python manage.py loaddata main_goal_fixture.json')
os.system('python manage.py loaddata type_food_fixture.json')
os.system('python manage.py loaddata difficulty_fixture.json')
os.system('python manage.py loaddata muscle_group_fixture.json')
os.system('python manage.py loaddata equipment_fixture.json')
os.system('python manage.py loaddata exercises_fixture.json')
os.system('python manage.py loaddata exercise_gif_fixture.json')

