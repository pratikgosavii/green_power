# Generated by Django 3.0.8 on 2022-04-06 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distributor', '0007_auto_20220406_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='distributor_payment_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(max_length=100)),
                ('payment_id', models.CharField(max_length=200)),
                ('distributor_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distributor.distributor_request', unique=True)),
            ],
        ),
    ]
