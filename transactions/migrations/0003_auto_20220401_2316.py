# Generated by Django 3.0.8 on 2022-04-01 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20220401_2315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bike_number',
            old_name='bike_number',
            new_name='chasis_no',
        ),
    ]
