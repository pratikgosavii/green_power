# Generated by Django 3.0.8 on 2022-04-01 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bike_number',
            old_name='chasis_no',
            new_name='bike_number',
        ),
    ]
