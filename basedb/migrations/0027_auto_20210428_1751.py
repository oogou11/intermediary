# Generated by Django 3.1.7 on 2021-04-28 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basedb', '0026_auto_20210428_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='choice_type',
            field=models.CharField(choices=[('0', '择优选取'), ('1', '竞价选取'), ('2', '平均价选取'), ('3', '线上谈判'), ('4', '线下谈判')], default='0', max_length=3, verbose_name='选取方式'),
        ),
    ]
