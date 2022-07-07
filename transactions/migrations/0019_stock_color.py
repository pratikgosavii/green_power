# Generated by Django 3.0.8 on 2022-07-06 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0004_auto_20220405_1720'),
        ('transactions', '0018_inward_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='color',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stores.Color'),
            preserve_default=False,
        ),
    ]
