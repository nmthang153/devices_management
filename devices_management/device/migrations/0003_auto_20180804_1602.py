# Generated by Django 2.0 on 2018-08-04 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0002_auto_20180804_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devices',
            name='keeper',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='devices',
            name='osType',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='devices',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='device.Project'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='version',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='device.devices'),
        ),
        migrations.AlterField(
            model_name='order',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='device.Project'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='close_at',
            field=models.DateField(null=True),
        ),
    ]
