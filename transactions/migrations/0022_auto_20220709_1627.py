# Generated by Django 3.0.8 on 2022-07-09 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0021_file_csv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file_csv',
            name='file_data',
            field=models.FileField(upload_to='media/'),
        ),
    ]
