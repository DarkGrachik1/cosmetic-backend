# Generated by Django 4.2.5 on 2023-12-19 21:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cosmetic',
            name='clinical_trial',
            field=models.IntegerField(blank=True, choices=[(1, 'Одобрено'), (2, 'Отказано')], null=True, verbose_name='Результат клинических испытаний'),
        ),
        migrations.AlterField(
            model_name='cosmetic',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 19, 21, 59, 24, 659762, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='substance',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='substances/', verbose_name='Картинка'),
        ),
    ]
