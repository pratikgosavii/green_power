# Generated by Django 3.0.8 on 2022-07-06 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0014_inward_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inward',
            name='color',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='color',
        ),
        migrations.AlterField(
            model_name='bike_number',
            name='chasis_no',
            field=models.CharField(blank=True, max_length=120, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='bike_number',
            name='controller_no',
            field=models.CharField(blank=True, max_length=120, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='bike_number',
            name='motor_no',
            field=models.CharField(blank=True, max_length=120, null=True, unique=True),
        ),
    ]
