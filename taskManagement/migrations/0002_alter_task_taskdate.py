# Generated by Django 3.2.25 on 2024-04-26 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskManagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='taskDate',
            field=models.DateTimeField(),
        ),
    ]
