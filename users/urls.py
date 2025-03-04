from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile')
]
