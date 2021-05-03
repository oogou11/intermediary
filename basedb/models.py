from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models
from django.utils import timezone
from django.conf import settings


class UserManager(BaseUserManager):
    def _create_user(self, username, password, email, **kwargs):
        if not username:
            raise ValueError("请传入用户名！")
        if not password:
            raise ValueError("请传入密码！")
        if not email:
            raise ValueError("请传入邮箱地址！")
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, email, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username, password, email, **kwargs)

    def create_superuser(self, username, password, email, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username, password, email, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):  # 继承AbstractBaseUser，PermissionsMixin

    STATUS_TYPE = (
        ("0", "正常"),
        ("1", "失信"),
        ("2", "黑名单"),
        ("3", "审核中"),
    )
    CUSTOMER_TYPE = (
        ("0", "管理员"),
        ("1", "业主"),
        ("2", "中介机构")
    )

    id = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=30, verbose_name="用户名", unique=True)
    customer_type = models.CharField(default="0",
                                     max_length=2, choices=CUSTOMER_TYPE, verbose_name="用户类型", null=True, blank=True)
    statustype = models.CharField(default="3",
                                  max_length=2, choices=STATUS_TYPE, verbose_name="用户状态", null=True, blank=True)
    phone = models.CharField(max_length=20,  verbose_name="手机号码")
    email = models.EmailField(verbose_name="邮箱", null=True, blank=True)
    contacts = models.CharField(default='',
                                max_length=30,  verbose_name="联系人姓名")
    cardid = models.CharField(default='', max_length=30, verbose_name="联系人身份证")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='加入时间', null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    rate = models.IntegerField(verbose_name='评价', default=0)
    servetype = models.ManyToManyField('servetype', default=None, verbose_name='服务事项')
    is_active = models.BooleanField(default=True, verbose_name="激活状态")
    is_staff = models.BooleanField(default=False, verbose_name="是否可以登录后台")
    is_union = models.BooleanField(default=False, verbose_name="是否联合体")
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    class Meta:
        managed = True
        verbose_name = "用户"
        db_table = 'user_info'
        verbose_name_plural = verbose_name

    @property
    def get_status_name(self):
        name = list(filter(lambda x: self.statustype == x[0], self.STATUS_TYPE))[0][1]
        return name

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True


class BaseModel(models.Model):
    '''抽象类'''
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')
    user = models.ForeignKey(
        User, null=True, blank=True, verbose_name='操作人', on_delete=models.SET_NULL)

    class Meta:
        abstract = True  # 抽象类


class ProprietorProfile(models.Model):
    """
    业主附件资料
    """
    STATUS_TYPE = (
        ("0", "草稿"),
        ("1", "待审核"),
        ("2", "已审核"),
        ("3", "驳回")
    )
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE,
                             related_name='proprietor_user')
    organization_code = models.CharField(max_length=100, verbose_name="统一社会信用代码/组织机构代码")
    organization_name = models.CharField(max_length=50, verbose_name="机构名称")
    corporation = models.CharField(max_length=100, verbose_name="法人")
    id_card_number = models.CharField(max_length=100, verbose_name="身份证号")
    organization_picture = models.JSONField(max_length=200, verbose_name='证件图片', null=True, blank=True)
    status = models.CharField(default='0', max_length=3, choices=STATUS_TYPE, verbose_name='状态')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    update_time = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')

    def __str__(self):
        return self.organization_name

    class Meta:
        verbose_name = "业主附件资料"
        verbose_name_plural = verbose_name


class SectionType(models.Model):
    """
    对应部门
    """
    id = ShortUUIDField(primary_key=True)
    parent_id = models.ForeignKey('self', null=True, blank=True, db_column='parent_id',
                                  verbose_name='上级部门', on_delete=models.SET_NULL)
    section_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='部门名称')

    def __str__(self):
        return self.section_name

    class Meta:
        verbose_name = "对应部门"
        verbose_name_plural = verbose_name


class ServeType(models.Model):
    """
    服务类型
    """
    id = models.AutoField(primary_key=True)
    section_id = models.ForeignKey(SectionType, null=True, blank=True, verbose_name='所属部门',
                                   db_column='section_id',
                                   on_delete=models.SET_NULL, related_name='service_bellow_section')
    picture_url = models.CharField(max_length=200, null=True, blank=True, verbose_name='图片')
    server_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='服务分类')
    is_root = models.BooleanField()

    def __str__(self):
        return self.server_name

    class Meta:
        verbose_name = "服务分类"
        verbose_name_plural = verbose_name


class IntermediaryProfile(models.Model):
    """
    中介机构附加资料
    """
    User_Qualifications = (
        ("0", "不限"),
        ("1", "甲级"),
        ("2", "已级"),
        ("3", "丙级"),
    )

    Status = (
        ("0", "初始化"),
        ("1", "待审核"),
        ("2", "审核通过"),
        ("3", "驳回"),
    )

    ENTERPRISE_TYPE = (
        ("0", "其他"),
        ("1", "社会"),
        ("2", "事业单位"),
        ("3", "政府机构"),
    )

    id = ShortUUIDField(primary_key=True)
    user = models.ForeignKey(to=User, verbose_name='用户', on_delete=models.CASCADE,
                             related_name='user_company')
    organization_code = models.CharField(max_length=100, verbose_name="统一社会信用代码/组织机构代码")
    organization_name = models.CharField(max_length=50, verbose_name="机构名称")
    corporation = models.CharField(max_length=20, verbose_name="法人")
    enterprise_type = models.CharField(max_length=3, null=True, blank=True, verbose_name='机构类型',
                                       choices=ENTERPRISE_TYPE)
    service_type = models.ManyToManyField(ServeType, verbose_name="服务类型")
    service_content = models.CharField(max_length=300, verbose_name="服务事项")
    address = models.CharField(max_length=100, verbose_name="公司地址")
    is_union = models.CharField(max_length=20, verbose_name='是否联合体')
    id_card_front_url = models.CharField(max_length=200, verbose_name='法人身份证正面', null=True, blank=True)
    id_card_back_url = models.CharField(max_length=200, verbose_name='法人身份证被面', null=True, blank=True)
    remark = models.CharField(max_length=200, verbose_name='备注')
    contract_person = models.CharField(max_length=50, verbose_name='联系人')
    co_id_card_front_url = models.CharField(max_length=200, verbose_name='联系人身份证正面', null=True, blank=True)
    co_id_card_back_url = models.CharField(max_length=200, verbose_name='联系人身份证被面', null=True, blank=True)
    authorize_url = models.CharField(max_length=200, verbose_name='授权书', null=True, blank=True)
    qualification_info = models.CharField(max_length=200, verbose_name='资质说明', choices=User_Qualifications,
                                          null=True, blank=True)
    qualification_list = models.JSONField(default=list, null=True, blank=True,
                                          max_length=400, verbose_name='资质证明')
    status = models.CharField(max_length=3, verbose_name='状态', choices=Status)
    update_time = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    super_rate = models.IntegerField(default=100, null=True, blank=True, verbose_name='上级评分')

    def __str__(self):
        return self.organization_name

    class Meta:
        verbose_name = "中介机构详情"
        verbose_name_plural = verbose_name


class AuditLog(models.Model):
    """
    审核日志
    """
    Audit_TYPE = (
        ('0', '业主信息'),
        ('1', '中介信息'),
        ('2', '项目信息'),
        ('3', '答疑信息')
    )
    Audit_Status = (
        ('0', '待审核'),
        ('2', '通过'),
        ('3', '驳回'),
    )
    id = ShortUUIDField(primary_key=True)
    user = models.ForeignKey(User, verbose_name='审核人', on_delete=models.SET_NULL,
                             db_constraint=False, null=True, blank=True)
    audit_type = models.CharField(max_length=3, verbose_name='审核类型', choices=Audit_TYPE)
    business_id = models.CharField(max_length=100, null=False, verbose_name='业务类型ID')
    content = models.CharField(max_length=100, null=True, blank=True, verbose_name="审核反馈")
    create_time = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name='创建时间')
    audit_time = models.DateTimeField(null=True, blank=True, verbose_name='审核时间')
    status = models.CharField(default='0', max_length=3, verbose_name='审核状态', choices=Audit_Status)

    class Meta:
        verbose_name = "审核记录"
        verbose_name_plural = verbose_name


class UserToken(models.Model):
    """
    存放用户Token
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_token')
    token = models.CharField(max_length=64, verbose_name="用户token")
    expiration_time = models.DateTimeField(verbose_name="过期时间")  # 默认过期时间24小时
    create_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Mate:
        db_table = "user_token"
        verbose_name = "用户Token"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.token


class Project(models.Model):
    """
    项目
    """
    STATUS_TYPE = (
        ("0", "用户草稿"),
        ("1", "待审核"),
        ("2", "竞标中"),
        ("3", "选标中"),
        ("4", "已选标"),
        ("5", "结束"),
        ("6", "作废"),
    )
    CHOICE_TYPE = (
        ("0", "择优选取"),
        ("1", "竞价选取"),
        ("2", "平均价选取"),
        ("3", "线上谈判"),
        ("4", "线下谈判"),

    )
    User_Qualifications = (
        ("0", "不限"),
        ("1", "甲级"),
        ("2", "已级"),
        ("3", "丙级"),
    )

    id = ShortUUIDField(primary_key=True)
    project_name = models.CharField(max_length=100, verbose_name='项目名称')
    contract_person = models.CharField(max_length=15, null=True, blank=True, verbose_name='联系人')
    contract_phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='联系电话')
    project_scale = models.IntegerField(verbose_name='预算金额')
    funds_source = models.CharField(max_length=100, null=True, blank=True, verbose_name='资金来源')
    project_limit = models.IntegerField(verbose_name='项目时限')
    service_low_count = models.IntegerField(verbose_name='服务金额下限')
    service_high_count = models.IntegerField(verbose_name='服务金额上限')
    content = models.CharField(max_length=800, verbose_name='服务内容')
    choice_type = models.CharField(default='0', max_length=3, choices=CHOICE_TYPE, verbose_name='选取方式')
    server_type = models.ManyToManyField(to=ServeType, verbose_name='所属服务类型')
    create_user = models.ForeignKey(to=User, verbose_name='创建人', on_delete=models.CASCADE,
                                    related_name='create_project')
    proprietor = models.ForeignKey(to=ProprietorProfile, null=True, blank=True,
                                   on_delete=models.SET_NULL, verbose_name='业主',
                                   related_name='project_proprietor')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    begin_time = models.DateTimeField(verbose_name='开始时间')
    finish_time = models.DateTimeField(verbose_name='竞标终止时间')

    qualification = models.CharField(default='0', max_length=50,
                                     choices=User_Qualifications, verbose_name='资质要求')
    remark = models.CharField(max_length=200, verbose_name='其他要求', null=True, blank=True)
    file_url = models.JSONField(max_length=200, verbose_name='上传文件', null=True, blank=True)
    status = models.CharField(default='0', max_length=3, choices=STATUS_TYPE, verbose_name='项目状态')
    contract = models.JSONField(max_length=200, default=None, null=True, blank=True, verbose_name='项目合同')
    score_level_one = models.IntegerField(default=0, verbose_name='一级服务评价')  # 满分5分
    score_level_two = models.IntegerField(default=0, verbose_name='二级服务评价')  # 满分5分
    score_level_three = models.IntegerField(default=0, verbose_name='三级服务评价')  # 满分5分
    score_level_four = models.IntegerField(default=0, verbose_name='四级服务评价')  # 满分5分
    score_level_five = models.IntegerField(default=0, verbose_name='五级服务评价')  # 满分5分
    average_score = models.FloatField(default=0, verbose_name='平均分')  # 平均分，保留一位
    project_message = models.CharField(max_length=200, null=True, blank=True, verbose_name='系统流标说明')
    equal_bid_company = models.JSONField(max_length=200, default=None, null=True, blank=True,
                                         verbose_name='系统无法选标中介机构')
    sys_info = models.CharField(max_length=200, verbose_name='系统任务说明!', null=True, blank=True)


    def __str__(self):
        return self.project_name

    class Meta:
        db_table = 'project'
        verbose_name = "项目信息"
        verbose_name_plural = verbose_name


class BidProject(models.Model):
    """
    竞标
    """
    STATUS = (
        ("0", "已投标"),
        ("1", "中标"),
    )
    id = ShortUUIDField(primary_key=True)
    project = models.ForeignKey(to=Project, verbose_name='竞标的项目', on_delete=models.CASCADE,
                                related_name='bid_projects')
    bid_user = models.ForeignKey(to=User, related_name='bid_users', verbose_name='竞标人员', on_delete=models.CASCADE)
    bid_company = models.ForeignKey(to=IntermediaryProfile, null=True, blank=False,
                                    related_name='bid_project_intermediary', on_delete=models.SET_NULL,
                                    verbose_name='竞标中介')
    bid_money = models.IntegerField(null=True, blank=True, verbose_name='竞标金额')
    files_info = models.JSONField(null=True, blank=True, verbose_name='竞标文件')
    describe = models.CharField(max_length=200, null=True, blank=True, verbose_name='竞标描述')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='竞标日期')
    update_time = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    status = models.CharField(max_length=2, default='0', choices=STATUS, verbose_name='竞标状态')
    owner_response = models.CharField(max_length=800, null=True, blank=True, verbose_name='业主回复')  # 业主回复
    is_active = models.BooleanField(default=True, verbose_name='是否有效')  # 新竞标 会作废旧的竞标

    class Meta:
        db_table = 'bid_project'
        verbose_name = "竞标项目"
        verbose_name_plural = verbose_name


class VerifyCode(models.Model):
    """
    短信发送信息
    """
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='手机号')
    verify_code = models.CharField(max_length=8, null=True, blank=True, verbose_name='验证码')
    send_time = models.DateTimeField(default=timezone.now, verbose_name='发送时间')
    expire_time = models.DateTimeField(null=True, blank=True, verbose_name='过期时间')


class MessageTemplate(models.Model):
    """
    短信模版
    """
    id = models.AutoField(primary_key=True)
    template_name = models.CharField(max_length=20, null=False, blank=False, verbose_name='模版名称')
    template_content = models.CharField(max_length=200, null=False, blank=False, verbose_name='模版内容')
    sms_type = models.IntegerField(default=0, verbose_name='短信类型 0:普通短信, 1:营销短信')
    international = models.IntegerField(default=0, verbose_name='0:国内短信,1:国际短信')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='模版备注')
    is_active = models.BooleanField(default=False, verbose_name='是否启动')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')


class MessageLog(models.Model):
    """
    短信访问IP记录地址
    """
    id = ShortUUIDField(primary_key=True)
    ip = models.CharField(max_length=100, null=False, blank=False, verbose_name='IP地址')
    count = models.IntegerField(default=0, null=False, blank=False, verbose_name='次数')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    update_time = models.DateTimeField(default=timezone.now, verbose_name='更新时间')
    limit_count = models.IntegerField(default=0, verbose_name='被限制次数')


class Interactive(models.Model):
    """
    竞标互动： 待删除
    """
    ACTIVE_TYPE = (
        (0, '业务主'),
        (1, '中介')
    )
    STATUS = (
        (0, '初始化'),
        (1, '业主回复')
    )

    id = ShortUUIDField(primary_key=True)
    project = models.ForeignKey(to=Project, verbose_name='竞标的项目', null=True, blank=True,
                                on_delete=models.SET_NULL, related_name='active_bid_projects')
    bid_user = models.ForeignKey(to=User, related_name='active_bid_users', verbose_name='竞标人员',
                                 null=True, blank=True, on_delete=models.SET_NULL)
    first_ask = models.JSONField(default=dict, verbose_name='第一次咨询')
    first_response = models.JSONField(default=dict, verbose_name='第一回复')
    second_ask = models.JSONField(default=dict, verbose_name='第二次咨询')
    second_response = models.JSONField(default=dict, verbose_name='第二回复')
    third_ask = models.JSONField(default=dict, verbose_name='第三次咨询')
    third_response = models.JSONField(default=dict, verbose_name='第三次回复')
    ask_count = models.IntegerField(default=1, verbose_name='咨询次数')
    response_count = models.IntegerField(default=0, verbose_name='回答次数')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='咨询时间')
    update_time = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
