# Generated by Django 3.1.7 on 2021-04-23 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basedb', '0003_auto_20210423_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='intermediaryprofile',
            name='update_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='更新时间'),
        ),
        migrations.AddField(
            model_name='proprietorprofile',
            name='update_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='更新时间'),
        ),
    ]
