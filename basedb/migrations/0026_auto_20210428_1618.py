# Generated by Django 3.1.7 on 2021-04-28 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basedb', '0025_auto_20210428_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_message',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='系统流标说明'),
        ),
    ]
