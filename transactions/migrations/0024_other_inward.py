# Generated by Django 3.0.8 on 2022-07-18 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0023_auto_20220709_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='other_inward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('GST_rate', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
