# Generated by Django 5.0.1 on 2024-01-30 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0007_quiz_groups_quiz_no_permission_students'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['-id']},
        ),
    ]
