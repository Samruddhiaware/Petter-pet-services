# Generated by Django 5.0.6 on 2024-07-05 17:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypetapp', '0005_remove_booking_cart_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='cart_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='mypetapp.cart'),
        ),
    ]
