# Generated by Django 5.2 on 2025-04-09 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_like_count_like_author_alter_like_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerlike',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='app.answer'),
        ),
        migrations.AlterField(
            model_name='answerlike',
            name='like',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.like'),
        ),
        migrations.AlterField(
            model_name='questionlike',
            name='like',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.like'),
        ),
        migrations.AlterField(
            model_name='questionlike',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='app.question'),
        ),
    ]
