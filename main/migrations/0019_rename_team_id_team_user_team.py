# Generated by Django 5.1.5 on 2025-04-30 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_team_user_team_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team_user',
            old_name='team_id',
            new_name='team',
        ),
    ]
