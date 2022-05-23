# Generated by Django 3.0.8 on 2022-04-08 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('showroom', '0005_auto_20220408_0145'),
    ]

    operations = [
        migrations.CreateModel(
            name='distributor_payment_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(max_length=100)),
                ('payment_id', models.CharField(max_length=200)),
                ('showroom_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='showroom.showroom_request', unique=True)),
            ],
        ),
    ]