from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import CustomUser, UserProfile, Gender, ActivityType, TypeFood, MainGoal, AdditionalGoal
from datetime import date


class RegisterForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'Пароли не совпадают.',  # Переопределяем сообщение об ошибке
    }
    first_name = forms.CharField(required=True, label='Имя',
                                 widget=forms.EmailInput(attrs={
                                     'class': 'u-grey-5 u-input u-input-rectangle u-radius u-input-1',
                                     'placeholder': 'Полное имя',
                                     'type': 'name'
                                 }))
    email = forms.EmailField(required=True, label='Email',
                             widget=forms.EmailInput(attrs={
                                 'class': 'u-grey-5 u-input u-input-rectangle u-radius u-input-1',
                                 'placeholder': 'Электронная почта',
                                 'type': 'email'
                             }))
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'u-grey-5 u-input u-input-rectangle u-radius u-input-1',
            'placeholder': 'Пароль',
            'type': 'password'
        })
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'u-grey-5 u-input u-input-rectangle u-radius u-input-1',
            'placeholder': 'Подтверждение пароля',
            'type': 'password'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Пароли не совпадают.")  # Добавляем ошибку к полю password2

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    gender = forms.ModelChoiceField(required=True,
                                    queryset=Gender.objects.all(),
                                    initial=Gender.objects.get(code='M'),
                                    widget=forms.Select(attrs={
                                        'class': 'u-input u-input-rectangle u-radius u-text-grey-80 u-input-1',
                                        'type': 'gender'}),
                                    label='Пол')

    date_of_birth = forms.DateField(required=True,
                                    widget=forms.DateInput(attrs={
                                        'class': 'u-input u-input-rectangle u-radius u-text-grey-80 u-input-2',
                                        'type': 'date',
                                        'placeholder': 'ДД-ММ-ГГГГ'}),
                                    label='Дата рождения')
    height = forms.FloatField(required=True,
                              widget=forms.NumberInput(attrs={
                                  'class': 'u-input u-input-rectangle u-radius u-text-grey-80 u-input-3',
                                  'placeholder': 'Введите ваш рост',
                                  'type': 'text'}),
                              label='Рост')
    weight = forms.FloatField(required=True,
                              widget=forms.NumberInput(attrs={
                                  'class': 'u-input u-input-rectangle u-radius u-text-grey-80 u-input-4',
                                  'placeholder': 'Введите ваш текущий вес',
                                  'type': 'text'}),
                              label='Текущий вес')
    desired_weight = forms.FloatField(required=True,
                                      widget=forms.NumberInput(attrs={
                                          'class': 'u-input u-input-rectangle u-radius u-text-grey-80 u-input-5',
                                          'placeholder': 'Введите ваш желаемый вес',
                                          'type': 'text'
                                      }),
                                      label='Желаемый вес')
    activity_type = forms.ModelChoiceField(required=True,
                                           queryset=ActivityType.objects.all(),
                                           initial=ActivityType.objects.get(name="Слегка активный"),
                                           widget=forms.Select(attrs={
                                               'class': 'u-input u-input-rectangle u-radius u-text-grey-80 u-input-6'
                                           }),
                                           label='Насколько вы активны?')
    type_food = forms.ModelChoiceField(required=True,
                                       queryset=TypeFood.objects.all(),
                                       initial=TypeFood.objects.get(name="Классический"),
                                       widget=forms.Select(attrs={
                                           'class': 'u-input u-input-rectangle u-radius u-text-grey-80 u-input-6'
                                       }),
                                       label='Вы хотите придерживаться какого-то определенного типа питания?')
    main_goal = forms.ModelChoiceField(required=True,
                                       queryset=MainGoal.objects.all(),
                                       initial=MainGoal.objects.get(name="Похудение"),
                                       widget=forms.Select(attrs={
                                           'class': 'u-input u-input-rectangle u-radius u-text-grey-80 u-input-7'
                                       }),
                                       label='Какова ваша главная цель?')
    additional_goal = forms.ModelMultipleChoiceField(required=True,
                                             queryset=AdditionalGoal.objects.all(),
                                             initial=AdditionalGoal.objects.get(name="Улучшить взаимоотношения с едой"),
                                             widget=forms.CheckboxSelectMultiple(attrs={
                                                 # 'class': 'u-active-palette-2-base u-field-input u-hover-palette-2-light-1 u-palette-2-base u-radius'
                                             }),
                                             label='У вас есть еще какие-то цели?')

    class Meta:
        model = UserProfile
        fields = ['gender', 'date_of_birth',
                  'height', 'weight', 'desired_weight',
                  'activity_type', 'type_food',
                  'main_goal', 'additional_goal']

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth >= date.today():
            raise forms.ValidationError('Дата рождения не может быть больше текущей даты.')
        return date_of_birth


class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}), label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(request=self.request, email=email, password=password)
            if user is None:
                raise forms.ValidationError('Неверный email или пароль.')
            return self.cleaned_data


