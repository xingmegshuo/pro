# Generated by Django 2.1 on 2020-03-25 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=20)),
                ('n_type', models.CharField(max_length=50)),
                ('unit', models.CharField(max_length=50)),
                ('unit_price', models.CharField(max_length=50)),
                ('quantity', models.CharField(max_length=50)),
                ('note', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu', models.CharField(max_length=50)),
                ('hard_disk', models.CharField(max_length=50)),
                ('video_memory', models.CharField(max_length=50)),
                ('memory', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='computer',
            name='info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.info'),
        ),
    ]
