# Generated by Django 3.0.8 on 2022-07-04 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showroom', '0014_auto_20220624_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='showroom_outward',
            name='bill_number',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='showroom_req',
            name='bill_number',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
