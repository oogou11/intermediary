# Generated by Django 3.1.7 on 2021-04-24 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basedb', '0012_auto_20210424_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='contract',
            field=models.JSONField(blank=True, max_length=200, null=True, verbose_name='项目合同'),
        ),
    ]
