# Generated by Django 5.2 on 2025-04-09 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_question_desc_alter_question_id_alter_question_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='like_count',
            field=models.IntegerField(default=1),
        ),
    ]
