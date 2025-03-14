from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, UserProfile, Gender, ActivityType, TypeFood, MainGoal, AdditionalGoal, BodyParameters, NutritionGoals
from datetime import date


class RegisterForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'Пароли не совпадают.',  # Переопределяем сообщение об ошибке
    }
    first_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField()
    password2 = forms.CharField()

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
                                    # initial=Gender.objects.get(code='M'),
                                    label='Пол')

    date_of_birth = forms.DateField(required=True,
                                    widget=forms.DateInput(),
                                    label='Дата рождения')
    height = forms.FloatField(required=True,
                              widget=forms.NumberInput(),
                              label='Рост')
    weight = forms.FloatField(required=True,
                              widget=forms.NumberInput(),
                              label='Текущий вес')
    desired_weight = forms.FloatField(required=True,
                                      widget=forms.NumberInput(),
                                      label='Желаемый вес')
    activity_type = forms.ModelChoiceField(required=True,
                                           queryset=ActivityType.objects.all(),
                                           # initial=ActivityType.objects.get(name="Слегка активный"),
                                           widget=forms.Select(),
                                           label='Насколько вы активны?')
    type_food = forms.ModelChoiceField(required=True,
                                       queryset=TypeFood.objects.all(),
                                       # initial=TypeFood.objects.get(name="Классический"),
                                       widget=forms.Select(),
                                       label='Вы хотите придерживаться какого-то определенного типа питания?')
    main_goal = forms.ModelChoiceField(required=True,
                                       queryset=MainGoal.objects.all(),
                                       # initial=MainGoal.objects.get(name="Похудение"),
                                       widget=forms.Select(),
                                       label='Какова ваша главная цель?')
    additional_goal = forms.ModelMultipleChoiceField(required=True,
                                             queryset=AdditionalGoal.objects.all(),
                                             # initial=AdditionalGoal.objects.get(name="Улучшить взаимоотношения с едой"),
                                             widget=forms.CheckboxSelectMultiple(),
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


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # Переопределяем поле username на email


class BodyParametersForm(forms.ModelForm):
    bmi = forms.NumberInput()
    weight = forms.FloatField(required=True, widget=forms.NumberInput(), label='Вес (кг)')
    desired_weight = forms.FloatField(required=True, widget=forms.NumberInput(), label='Желаемый вес (кг)')
    chest = forms.NumberInput()
    waist = forms.NumberInput()
    hips = forms.NumberInput()
    thigh = forms.NumberInput()
    biceps = forms.NumberInput()

    class Meta:
        model = BodyParameters
        fields = ['weight', 'desired_weight', 'chest', 'waist', 'hips', 'thigh', 'biceps']


class NutritionGoalsForm(forms.ModelForm):
    class Meta:
        model = NutritionGoals
        fields = ['target_kcal', 'target_protein', 'target_fat', 'target_carb']
        labels = {
            'target_kcal': 'Целевые калории (ккал)',
            'target_protein': 'Целевые белки (г)',
            'target_fat': 'Целевые жиры (г)',
            'target_carb': 'Целевые углеводы (г)',
        }

