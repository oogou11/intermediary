# Generated by Django 3.1.7 on 2021-04-24 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basedb', '0010_auto_20210424_1509'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_uni',
            new_name='is_union',
        ),
    ]
