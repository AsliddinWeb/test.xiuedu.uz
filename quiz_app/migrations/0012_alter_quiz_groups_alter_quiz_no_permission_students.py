# Generated by Django 5.0.1 on 2024-02-13 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0011_alter_question_subject'),
        ('student_app', '0012_alter_group_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='groups',
            field=models.ManyToManyField(blank=True, to='student_app.group'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='no_permission_students',
            field=models.ManyToManyField(blank=True, to='student_app.student'),
        ),
    ]
