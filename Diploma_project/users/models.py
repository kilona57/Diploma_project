from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from datetime import date


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, password, confirm_password):
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Password is required')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, confirrm_password=confirm_password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password, confirm_password):
        user = self.create_user(email, first_name, password, confirm_password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, verbose_name='first name')
    email = models.EmailField(unique=True, verbose_name='email')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Gender(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    code = models.CharField(max_length=1, unique=True, verbose_name='Код')

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'

    def __str__(self):
        return self.name


class ActivityType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Вид активности'
        verbose_name_plural = 'Виды активности'

    def __str__(self):
        return self.name


class MainGoal(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Главная цель'
        verbose_name_plural = 'Главные цели'

    def __str__(self):
        return self.name


class TypeFood(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Тип питания'
        verbose_name_plural = 'Типы питания'

    def __str__(self):
        return self.name


class AdditionalGoal(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Дополнительная цель'
        verbose_name_plural = 'Дополнительные цели'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пол')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    height = models.FloatField(null=True, blank=True, verbose_name='Рост')
    weight = models.FloatField(null=True, blank=True, verbose_name='Вес')
    desired_weight = models.FloatField(null=True, blank=True, verbose_name='Желаемый вес')
    activity_type = models.ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='Тип активности')
    type_food = models.ForeignKey(TypeFood, on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name='Тип питания')
    main_goal = models.ForeignKey(MainGoal, on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name='Главная цель')
    additional_goal = models.ManyToManyField(AdditionalGoal, blank=True, verbose_name='Дополнительные цели')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

    def age_with_suffix(self):
        if self.age is None:
            return "Не указан"

        age = int(self.age)
        last_digit = age % 10
        last_two_digits = age % 100

        if 11 <= last_two_digits <= 19:
            suffix = "лет"
        elif last_digit == 1:
            suffix = "год"
        elif 2 <= last_digit <= 4:
            suffix = "года"
        else:
            suffix = "лет"

        return f"{age} {suffix}"

    def __str__(self):
        return f"Профиль {self.user.email}"


class BodyParameters(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='body_parameters')
    bmi = models.FloatField(verbose_name='ИМТ', null=True, blank=True)
    chest = models.FloatField(verbose_name='Объем груди (см)', null=True, blank=True)
    waist = models.FloatField(verbose_name='Объем талии (см)', null=True, blank=True)
    hips = models.FloatField(verbose_name='Объем бедер (см)', null=True, blank=True)
    thigh = models.FloatField(verbose_name='Объем бедра (см)', null=True, blank=True)
    biceps = models.FloatField(verbose_name='Объем бицепса (см)', null=True, blank=True)

    def calculate_bmi(self):
        user_profile = self.user.profile
        if user_profile.height and user_profile.weight:
            self.bmi = round(user_profile.weight / ((user_profile.height / 100) ** 2), 2)
        else:
            self.bmi = None

    def save(self, *args, **kwargs):
        self.calculate_bmi()  # Пересчитываем ИМТ перед сохранением
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'Параметры тела'
        verbose_name_plural = 'Параметры тела'

    def __str__(self):
        return (f"Параметры тела пользователя {self.user.username}")

class NutritionGoals(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='nutrition_goals')
    target_kcal = models.FloatField(verbose_name='Целевые калории (ккал)', null=True, blank=True)
    target_protein = models.FloatField(verbose_name='Целевые белки (г)', null=True, blank=True)
    target_fat = models.FloatField(verbose_name='Целевые жиры (г)', null=True, blank=True)
    target_carb = models.FloatField(verbose_name='Целевые углеводы (г)', null=True, blank=True)

    class Meta:
        verbose_name = 'Цели по КБЖУ'
        verbose_name_plural = 'Цели по КБЖУ'

    def __str__(self):
        return f"Цели по КБЖУ для {self.user.email}"