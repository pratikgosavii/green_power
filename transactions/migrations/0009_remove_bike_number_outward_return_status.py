# Generated by Django 3.0.8 on 2022-06-20 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0008_auto_20220620_0226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bike_number_outward',
            name='return_status',
        ),
    ]