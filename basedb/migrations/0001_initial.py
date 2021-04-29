# Generated by Django 3.1.7 on 2021-04-23 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='用户名')),
                ('customer_type', models.CharField(blank=True, choices=[('0', '管理员'), ('1', '业主'), ('2', '中介机构')], default='0', max_length=2, null=True, verbose_name='用户类型')),
                ('statustype', models.CharField(blank=True, choices=[('0', '正常'), ('1', '失信'), ('2', '黑名单'), ('3', '审核中')], default='3', max_length=2, null=True, verbose_name='用户状态')),
                ('phone', models.CharField(max_length=20, verbose_name='手机号码')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱')),
                ('contacts', models.CharField(default='', max_length=30, verbose_name='联系人姓名')),
                ('cardid', models.CharField(default='', max_length=30, verbose_name='联系人身份证')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('rate', models.IntegerField(default=0, verbose_name='评价')),
                ('is_active', models.BooleanField(default=True, verbose_name='激活状态')),
                ('is_staff', models.BooleanField(default=False, verbose_name='是否可以登录后台')),
                ('is_uni', models.BooleanField(default=False, verbose_name='是否联合体')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'user_info',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MessageLog',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('ip', models.CharField(max_length=100, verbose_name='IP地址')),
                ('count', models.IntegerField(default=0, verbose_name='次数')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='更新时间')),
                ('limit_count', models.IntegerField(default=0, verbose_name='被限制次数')),
            ],
        ),
        migrations.CreateModel(
            name='MessageTemplate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('template_name', models.CharField(max_length=20, verbose_name='模版名称')),
                ('template_content', models.CharField(max_length=200, verbose_name='模版内容')),
                ('sms_type', models.IntegerField(default=0, verbose_name='短信类型 0:普通短信, 1:营销短信')),
                ('international', models.IntegerField(default=0, verbose_name='0:国内短信,1:国际短信')),
                ('remark', models.CharField(blank=True, max_length=200, null=True, verbose_name='模版备注')),
                ('is_active', models.BooleanField(default=False, verbose_name='是否启动')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='SectionType',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('parent_id', models.CharField(max_length=50, verbose_name='父节点ID')),
                ('section_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='部门名称')),
            ],
            options={
                'verbose_name': '对应部门',
                'verbose_name_plural': '对应部门',
            },
        ),
        migrations.CreateModel(
            name='VerifyCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='手机号')),
                ('verify_code', models.CharField(blank=True, max_length=8, null=True, verbose_name='验证码')),
                ('send_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发送时间')),
                ('expire_time', models.DateTimeField(blank=True, null=True, verbose_name='过期时间')),
            ],
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64, verbose_name='用户token')),
                ('expiration_time', models.DateTimeField(verbose_name='过期时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_token', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServeType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('server_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='服务分类')),
                ('is_root', models.BooleanField()),
                ('section_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basedb.sectiontype', verbose_name='所属部门')),
            ],
            options={
                'verbose_name': '服务分类',
                'verbose_name_plural': '服务分类',
            },
        ),
        migrations.CreateModel(
            name='ProprietorProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_code', models.CharField(max_length=100, verbose_name='统一社会信用代码/组织机构代码')),
                ('organization_name', models.CharField(max_length=50, verbose_name='机构名称')),
                ('corporation', models.CharField(max_length=100, verbose_name='法人')),
                ('id_card_number', models.CharField(max_length=100, verbose_name='身份证号')),
                ('organization_picture', models.CharField(blank=True, max_length=200, verbose_name='证件图片')),
                ('status', models.CharField(choices=[('0', '待审核'), ('2', '已审核'), ('3', '驳回')], default='0', max_length=3, verbose_name='状态')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '业主附件资料',
                'verbose_name_plural': '业主附件资料',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=100, verbose_name='项目名称')),
                ('contract_person', models.CharField(max_length=15, verbose_name='联系人')),
                ('project_scale', models.CharField(max_length=15, verbose_name='项目规模')),
                ('project_limit', models.IntegerField(verbose_name='项目时限')),
                ('service_low_count', models.FloatField(verbose_name='服务金额下限')),
                ('service_high_count', models.FloatField(verbose_name='服务金额上限')),
                ('content', models.CharField(max_length=800, verbose_name='服务内容')),
                ('choice_type', models.CharField(choices=[('0', '择优选取'), ('1', '竞价选取'), ('2', '平均价选取'), ('3', '三次交互选取')], default='0', max_length=3, verbose_name='选取方式')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('begin_time', models.DateTimeField(verbose_name='开始时间')),
                ('finish_time', models.DateTimeField(verbose_name='竞标终止时间')),
                ('qualification', models.CharField(choices=[('0', '不限'), ('1', '甲级'), ('2', '已级'), ('3', '丙级')], default='0', max_length=50, verbose_name='资质要求')),
                ('remark', models.CharField(max_length=200, verbose_name='其他要求')),
                ('file_url', models.CharField(max_length=20, verbose_name='上传文件')),
                ('status', models.CharField(choices=[('0', '初始化'), ('1', '待审核'), ('2', '审核通过'), ('3', '驳回')], default='0', max_length=3, verbose_name='项目状态')),
                ('sys_info', models.CharField(max_length=200, verbose_name='系统任务说明!')),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create_project', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
            ],
            options={
                'verbose_name': '项目信息',
                'verbose_name_plural': '项目信息',
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='IntermediaryProfile',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('organization_code', models.CharField(max_length=100, verbose_name='统一社会信用代码/组织机构代码')),
                ('organization_name', models.CharField(max_length=50, verbose_name='机构名称')),
                ('corporation', models.CharField(max_length=20, verbose_name='法人')),
                ('service_content', models.CharField(max_length=300, verbose_name='服务事项')),
                ('address', models.CharField(max_length=100, verbose_name='公司地址')),
                ('is_union', models.CharField(max_length=20, verbose_name='是否联合体')),
                ('id_card_front_url', models.CharField(blank=True, max_length=200, null=True, verbose_name='法人身份证正面')),
                ('id_card_back_url', models.CharField(blank=True, max_length=200, null=True, verbose_name='法人身份证被面')),
                ('remark', models.CharField(max_length=200, verbose_name='备注')),
                ('contract_person', models.CharField(max_length=50, verbose_name='联系人')),
                ('co_id_card_front_url', models.CharField(blank=True, max_length=200, null=True, verbose_name='联系人身份证正面')),
                ('co_id_card_back_url', models.CharField(blank=True, max_length=200, null=True, verbose_name='联系人身份证被面')),
                ('authorize_url', models.CharField(blank=True, max_length=200, null=True, verbose_name='授权书')),
                ('qualification_info', models.CharField(blank=True, choices=[('0', '不限'), ('1', '甲级'), ('2', '已级'), ('3', '丙级')], max_length=200, null=True, verbose_name='资质说明')),
                ('qualification_list', models.JSONField(default=list, max_length=200, verbose_name='资质证明')),
                ('status', models.CharField(choices=[('0', '初始化'), ('1', '待审核'), ('2', '审核通过'), ('3', '驳回')], max_length=200, verbose_name='状态')),
                ('service_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_service_type', to='basedb.servetype', verbose_name='服务类型')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_company', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '中介机构详情',
                'verbose_name_plural': '中介机构详情',
            },
        ),
        migrations.CreateModel(
            name='Interactive',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('first_ask', models.JSONField(default=dict, verbose_name='第一次咨询')),
                ('first_response', models.JSONField(default=dict, verbose_name='第一回复')),
                ('second_ask', models.JSONField(default=dict, verbose_name='第二次咨询')),
                ('second_response', models.JSONField(default=dict, verbose_name='第二回复')),
                ('third_ask', models.JSONField(default=dict, verbose_name='第三次咨询')),
                ('third_response', models.JSONField(default=dict, verbose_name='第三次回复')),
                ('active_count', models.IntegerField(default=0, verbose_name='互动次数')),
                ('status', models.BooleanField(default=False, verbose_name='是否交互完成')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='咨询时间')),
                ('update_time', models.DateTimeField(blank=True, null=True, verbose_name='更新时间')),
                ('bid_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='active_bid_users', to=settings.AUTH_USER_MODEL, verbose_name='竞标人员')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='active_bid_projects', to='basedb.project', verbose_name='竞标的项目')),
            ],
        ),
        migrations.CreateModel(
            name='BidProject',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('bid_money', models.FloatField(verbose_name='竞标金额')),
                ('describe', models.CharField(max_length=200, verbose_name='竞标描述')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='竞标日期')),
                ('update_time', models.DateTimeField(verbose_name='更新时间')),
                ('update_number', models.IntegerField(default=0, verbose_name='更新次数')),
                ('status', models.CharField(choices=[('0', '参与竞标'), ('1', '中标')], default='0', max_length=2, verbose_name='竞标状态')),
                ('score_level_one', models.IntegerField(default=0, verbose_name='一级服务评价')),
                ('score_level_two', models.IntegerField(default=0, verbose_name='一级服务评价')),
                ('score_level_three', models.IntegerField(default=0, verbose_name='一级服务评价')),
                ('score_level_four', models.IntegerField(default=0, verbose_name='服务评价')),
                ('score_level_five', models.IntegerField(default=0, verbose_name='服务评价')),
                ('bid_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_users', to=settings.AUTH_USER_MODEL, verbose_name='竞标人员')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_projects', to='basedb.project', verbose_name='竞标的项目')),
            ],
            options={
                'verbose_name': '竞标项目',
                'verbose_name_plural': '竞标项目',
                'db_table': 'bid_project',
            },
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('audit_type', models.CharField(choices=[('0', '业主信息'), ('1', '中介信息'), ('2', '项目信息'), ('3', '答疑信息')], max_length=3, verbose_name='审核类型')),
                ('business_id', models.CharField(max_length=100, verbose_name='业务类型ID')),
                ('content', models.CharField(blank=True, max_length=100, null=True, verbose_name='审核反馈')),
                ('create_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='创建时间')),
                ('audit_time', models.DateTimeField(blank=True, null=True, verbose_name='审核时间')),
                ('status', models.CharField(choices=[('0', '待审核'), ('2', '通过'), ('3', '驳回')], default='0', max_length=3, verbose_name='审核状态')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='审核人')),
            ],
            options={
                'verbose_name': '审核记录',
                'verbose_name_plural': '审核记录',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='servetype',
            field=models.ManyToManyField(default=None, to='basedb.ServeType', verbose_name='服务事项'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]