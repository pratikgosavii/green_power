# Generated by Django 3.0.8 on 2022-04-06 06:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0004_auto_20220405_1720'),
        ('distributor', '0003_auto_20220406_0257'),
    ]

    operations = [
        migrations.CreateModel(
            name='distributor_req',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bike_qty', models.IntegerField()),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dcdxcdvfes', to='stores.Color')),
            ],
        ),
        migrations.RemoveField(
            model_name='distributor_request',
            name='bike_qty',
        ),
        migrations.RemoveField(
            model_name='distributor_request',
            name='color',
        ),
        migrations.RemoveField(
            model_name='distributor_request',
            name='distributor_request_log',
        ),
        migrations.RemoveField(
            model_name='distributor_request',
            name='variant',
        ),
        migrations.AddField(
            model_name='distributor_request',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='distributor_request',
            name='distributor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='dfdscf', to='stores.distributor'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='distributor_request_log',
        ),
        migrations.AddField(
            model_name='distributor_req',
            name='distributor_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distributor.distributor_request'),
        ),
        migrations.AddField(
            model_name='distributor_req',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sdssfsfdf', to='stores.variant'),
        ),
    ]
