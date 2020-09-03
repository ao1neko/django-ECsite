# Generated by Django 3.0.7 on 2020-08-27 05:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecsitecore', '0006_auto_20200827_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='star',
        ),
        migrations.AddField(
            model_name='review',
            name='score',
            field=models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='スコア'),
        ),
    ]