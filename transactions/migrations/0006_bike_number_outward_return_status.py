# Generated by Django 3.0.8 on 2022-06-19 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_bike_number_outward_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='bike_number_outward',
            name='return_status',
            field=models.BooleanField(default=False),
        ),
    ]
