# Generated by Django 5.1.3 on 2024-12-15 14:37

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=120)),
                ('logo', models.ImageField(default='restaurants/default.jpg', upload_to='restaurants')),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=1000)),
                ('call_number', models.CharField(max_length=16)),
                ('rate', models.CharField(choices=[('1', 'very bad'), ('2', 'bad'), ('3', 'natural'), ('4', 'good'), ('5', 'very good')], default='5', max_length=1)),
                ('time_to_open', models.TimeField()),
                ('time_to_close', models.TimeField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurants', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
