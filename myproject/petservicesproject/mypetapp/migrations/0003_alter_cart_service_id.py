# Generated by Django 5.0.6 on 2024-07-05 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypetapp', '0002_alter_spservice_managers_spservice_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='service_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mypetapp.spservice'),
        ),
    ]