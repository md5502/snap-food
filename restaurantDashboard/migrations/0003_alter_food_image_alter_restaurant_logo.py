# Generated by Django 5.1.3 on 2024-12-10 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantDashboard', '0002_alter_foodcomment_restaurant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='image',
            field=models.ImageField(default='foods/default.jpg', upload_to='foods'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='logo',
            field=models.ImageField(default='restaurants/default.jpg', upload_to='restaurants'),
        ),
    ]
