# Generated by Django 5.0.1 on 2024-01-22 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0004_alter_grade_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['-id']},
        ),
    ]
