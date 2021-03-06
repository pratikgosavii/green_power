# Generated by Django 3.0.8 on 2022-04-05 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0004_auto_20220405_1720'),
        ('distributor', '0002_distributor_stock_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distributor_request',
            name='date',
        ),
        migrations.RemoveField(
            model_name='distributor_request',
            name='distributor',
        ),
        migrations.CreateModel(
            name='distributor_request_log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('distributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dfdscf', to='stores.distributor')),
            ],
        ),
        migrations.AddField(
            model_name='distributor_request',
            name='distributor_request_log',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='distributor.distributor_request_log'),
            preserve_default=False,
        ),
    ]
