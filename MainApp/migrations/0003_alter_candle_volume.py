# Generated by Django 4.1.3 on 2023-12-05 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0002_alter_candle_volume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candle',
            name='volume',
            field=models.IntegerField(),
        ),
    ]
