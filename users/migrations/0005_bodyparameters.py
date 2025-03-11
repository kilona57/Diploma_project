# Generated by Django 5.1.6 on 2025-03-06 19:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyParameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bmi', models.FloatField(blank=True, null=True, verbose_name='ИМТ')),
                ('chest', models.FloatField(blank=True, null=True, verbose_name='Объем груди (см)')),
                ('waist', models.FloatField(blank=True, null=True, verbose_name='Объем талии (см)')),
                ('hips', models.FloatField(blank=True, null=True, verbose_name='Объем бедер (см)')),
                ('thigh', models.FloatField(blank=True, null=True, verbose_name='Объем бедра (см)')),
                ('biceps', models.FloatField(blank=True, null=True, verbose_name='Объем бицепса (см)')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='body_parameters', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Параметры тела',
                'verbose_name_plural': 'Параметры тела',
            },
        ),
    ]
