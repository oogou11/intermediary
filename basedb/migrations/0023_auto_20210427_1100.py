# Generated by Django 3.1.7 on 2021-04-27 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basedb', '0022_auto_20210427_1057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='owner_response',
        ),
        migrations.AddField(
            model_name='bidproject',
            name='owner_response',
            field=models.JSONField(default=list, verbose_name='业主回复'),
        ),
    ]
