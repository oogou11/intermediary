# Generated by Django 3.1.7 on 2021-04-25 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basedb', '0018_auto_20210425_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='servetype',
            name='picture_url',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='图片'),
        ),
    ]
