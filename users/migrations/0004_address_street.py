# Generated by Django 5.1.3 on 2024-12-23 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='street',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]