# Generated by Django 2.0 on 2018-08-05 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0004_supplement'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplement',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]