# Generated by Django 5.1.3 on 2024-12-10 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(default='profile_images/default.jpg', upload_to='profile_images'),
        ),
    ]