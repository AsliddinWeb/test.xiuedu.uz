# Generated by Django 5.0.1 on 2024-01-20 10:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='grade',
        ),
        migrations.AddField(
            model_name='group',
            name='grade',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='student_app.grade'),
            preserve_default=False,
        ),
    ]
