# Generated by Django 2.2 on 2020-05-29 03:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='M_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 29, 11, 8, 35, 837352), verbose_name='评论时间'),
        ),
    ]