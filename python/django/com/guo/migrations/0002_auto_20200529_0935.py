# Generated by Django 2.2 on 2020-05-29 01:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('guo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='M_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 29, 1, 35, 0, 393214, tzinfo=utc), verbose_name='评论时间'),
        ),
    ]
