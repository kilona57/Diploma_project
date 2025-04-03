from django.urls import path
from workouts import views


urlpatterns = [
    path('', views.exercises, name='generate_training'),
]
