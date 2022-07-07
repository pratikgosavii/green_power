# Generated by Django 3.0.8 on 2022-07-06 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0004_auto_20220405_1720'),
        ('transactions', '0011_auto_20220704_1728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bike_number',
            name='color',
        ),
        migrations.AddField(
            model_name='inward',
            name='color',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stores.Color'),
            preserve_default=False,
        ),
    ]
