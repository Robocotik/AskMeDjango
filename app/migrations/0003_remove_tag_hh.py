# Generated by Django 5.2 on 2025-04-09 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_profile_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='hh',
        ),
    ]
