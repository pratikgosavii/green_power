# Generated by Django 3.0.8 on 2022-06-21 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0009_remove_bike_number_outward_return_status'),
        ('showroom', '0009_auto_20220621_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showroom_bike_number_return',
            name='bike_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sdsdsdwwwd', to='transactions.bike_number'),
        ),
    ]
