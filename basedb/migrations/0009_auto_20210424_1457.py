# Generated by Django 3.1.7 on 2021-04-24 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basedb', '0008_auto_20210424_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidproject',
            name='bid_company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bid_project_intermediary', to='basedb.intermediaryprofile', verbose_name='竞标中介'),
        ),
        migrations.AlterField(
            model_name='project',
            name='file_url',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='上传文件'),
        ),
        migrations.AlterField(
            model_name='project',
            name='remark',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='其他要求'),
        ),
        migrations.AlterField(
            model_name='project',
            name='sys_info',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='系统任务说明!'),
        ),
    ]
