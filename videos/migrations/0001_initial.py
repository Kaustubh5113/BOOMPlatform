# Generated by Django 5.2.1 on 2025-05-25 05:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('video_type', models.CharField(choices=[('short', 'Short Form'), ('long', 'Long Form')], max_length=10)),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('video_url', models.URLField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.video')),
            ],
        ),
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('gifter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gifts_given', to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.video')),
            ],
        ),
    ]
