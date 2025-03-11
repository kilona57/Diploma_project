# Generated by Django 5.1.6 on 2025-03-09 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_bodyparameters'),
    ]

    operations = [
        migrations.AddField(
            model_name='bodyparameters',
            name='height',
            field=models.FloatField(default=0.0, verbose_name='Рост (см)'),
        ),
        migrations.AddField(
            model_name='bodyparameters',
            name='weight',
            field=models.FloatField(default=0.0, verbose_name='Вес (кг)'),
        ),
    ]
