# Generated by Django 5.1.5 on 2025-04-25 09:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_team_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to='main.company'),
        ),
    ]
