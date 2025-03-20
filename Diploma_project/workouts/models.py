from django.db import models
from users.models import CustomUser


class MuscleGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название группы мышц")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа мышц"
        verbose_name_plural = "Группы мышц"


class Equipment(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название оборудования")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"


class Difficulty(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название сложности")
    description = models.TextField(verbose_name="Описание сложности", blank=True, null=True)
    level = models.PositiveIntegerField(verbose_name="Уровень сложности", help_text="Чем выше число, тем сложнее упражнение")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сложность"
        verbose_name_plural = "Сложности"


class Exercise(models.Model):
    # Основные поля
    name = models.CharField(max_length=255, verbose_name="Название упражнения")

    muscle_group = models.ForeignKey(
        MuscleGroup,
        on_delete=models.SET_NULL,
        verbose_name="Группа мышц",
        blank=True,
        null=True,
        related_name="exercises"
    )

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.SET_NULL,
        verbose_name="Оборудование",
        blank=True,
        null=True,
        related_name="exercises"
    )
    description = models.TextField(verbose_name="Описание упражнения", blank=True, null=True)
    difficulty = models.ForeignKey(
        Difficulty,
        on_delete=models.SET_NULL,
        verbose_name="Сложность",
        blank=True,
        null=True,
        related_name="exercises"
    )
    calories_burned = models.PositiveIntegerField(verbose_name="Количество затрачиваемых калорий")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Упражнение"
        verbose_name_plural = "Упражнения"


class ExerciseGif(models.Model):
    exercise = models.ForeignKey(
        'Exercise',
        on_delete=models.CASCADE,
        verbose_name="Упражнение",
        related_name="gifs"
    )
    gif_name = models.CharField(
        max_length=255,
        verbose_name="Имя GIF-файла",
        help_text="Имя файла в папке static/gif"
    )

    def __str__(self):
        return f"GIF для {self.exercise.name}"

    class Meta:
        verbose_name = "GIF-изображение"
        verbose_name_plural = "GIF-изображения"


class TypeOfWorkout(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Тип тренировки",
        unique=True,
    )

    def __str__(self):
        return f"Тип тренировки: {self.name}"

    class Meta:
        verbose_name = "Тип тренировки"
        verbose_name_plural = "Типы тренировок"


class DayNumber(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Номер дня",
        unique=True,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "День тренировки"
        verbose_name_plural = "Дни тренеровок"


class Training(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="user"
    )
    type_of_workout = models.ForeignKey(
        TypeOfWorkout,
        on_delete=models.CASCADE,
        verbose_name="Тип тренировки",
        related_name="type_of_workout"
    )

    def __str__(self):
        return f"Пользователь: {self.user}, тип тренировки: {self.type_of_workout}"

    class Meta:
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"


class TrainingSchedule(models.Model):
    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        verbose_name="Тренировка",
        related_name="training"
    )
    day_number = models.ForeignKey(
        DayNumber,
        on_delete=models.CASCADE,
        verbose_name="День",
        related_name="day"
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        verbose_name="Упражнение",
        related_name="exercise"
    )
    repeat = models.IntegerField(
        verbose_name='Количество повторений',
    )
    approaches = models.IntegerField(
        verbose_name='Количество подходов',
    )

    def __str__(self):
        return f"День: {self.day_number}, " \
               f"упражнение: {self.exercise}" \
               f"количество повторений: {self.repeat}" \
               f"количество подходов: {self.approaches}"

    class Meta:
        verbose_name = "Расписание тренировки"
        verbose_name_plural = "Расписание тренировок"
