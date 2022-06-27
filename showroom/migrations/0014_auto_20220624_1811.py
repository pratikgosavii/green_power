# Generated by Django 3.0.8 on 2022-06-24 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0009_remove_bike_number_outward_return_status'),
        ('distributor', '0022_distributor_bike_number_return_company_outward'),
        ('showroom', '0013_auto_20220624_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showroom_bike_number_return',
            name='outward_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transactions.outward'),
        ),
        migrations.AlterField(
            model_name='showroom_bike_number_return',
            name='outward_distributor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='distributor.distributor_outward'),
        ),
    ]