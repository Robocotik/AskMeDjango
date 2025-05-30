# Generated by Django 5.2 on 2025-04-09 09:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_like_author_remove_like_question_like_count'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='app.question'),
        ),
        migrations.AlterField(
            model_name='answerlike',
            name='answer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='app.answer'),
        ),
        migrations.AlterField(
            model_name='answerlike',
            name='like',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.like'),
        ),
        migrations.AlterField(
            model_name='question',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='questionlike',
            name='like',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.like'),
        ),
        migrations.AlterField(
            model_name='questionlike',
            name='question',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='app.question'),
        ),
    ]
