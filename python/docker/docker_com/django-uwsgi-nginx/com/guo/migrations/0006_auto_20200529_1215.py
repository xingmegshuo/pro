# Generated by Django 2.2 on 2020-05-29 04:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('guo', '0005_auto_20200529_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='M_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='评论时间'),
        ),
    ]