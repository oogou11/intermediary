# Generated by Django 3.1.7 on 2021-04-24 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basedb', '0009_auto_20210424_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='file_url',
            field=models.JSONField(blank=True, max_length=200, null=True, verbose_name='上传文件'),
        ),
    ]
