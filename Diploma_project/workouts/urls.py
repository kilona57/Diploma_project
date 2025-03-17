from django.urls import path
from . import views


urlpatterns = [
    path('', views.generate_training, name='generate_training'),
]
