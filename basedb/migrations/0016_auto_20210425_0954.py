# Generated by Django 3.1.7 on 2021-04-25 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basedb', '0015_auto_20210425_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidproject',
            name='update_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='更新时间'),
        ),
    ]
