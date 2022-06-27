# Generated by Django 3.0.8 on 2022-06-19 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_auto_20220620_0223'),
        ('distributor', '0013_remove_distributor_bike_number_outward_return_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distributor_bike_number_outward',
            name='bike_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.bike_number'),
        ),
    ]
