# Generated by Django 3.0.7 on 2020-08-27 08:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecsitecore', '0007_auto_20200827_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='phon',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Tel Number must be entered in the format: '09012345678'. Up to 15 digits allowed.", regex='^[0-9]+$')], verbose_name='電話番号'),
        ),
    ]