# Generated by Django 5.0.1 on 2024-01-22 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0009_group_type_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='type_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='student_app.typegroup'),
        ),
    ]
