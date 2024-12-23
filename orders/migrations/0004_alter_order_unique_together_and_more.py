# Generated by Django 5.1.3 on 2024-12-23 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_orderitem_total_price'),
        ('users', '0004_address_street'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.address'),
        ),
    ]
