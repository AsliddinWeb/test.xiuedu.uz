# Generated by Django 5.0.1 on 2024-03-04 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0018_result_random_quizes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='random_quizes',
            field=models.ManyToManyField(to='quiz_app.question'),
        ),
    ]