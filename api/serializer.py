from rest_framework import serializers
from drf_yasg import openapi
from django.utils.translation import gettext_lazy as _


class RegisterSerializer(serializers.Serializer):
    """
    注册序列化参数
    """
    username = serializers.CharField(
        label=_("用户名"),
        required=True
    )
    password = serializers.CharField(
        label=_("密码"),
        style={'input_type': 'password'},
        required=True
    )
    email = serializers.CharField(
        label=_("邮箱"),
        required=True
    )
    phone = serializers.CharField(
        label=_("电话"),
        required=True,
    )
    verify_code = serializers.CharField(
        label=_("验证码"),
        required=False,
        help_text='变更手机号需要验证码'
    )
    customer_type = serializers.ChoiceField(
        label=_("用户类型"),
        choices=['1', '2'],
        help_text='"1":"业主", "2":"中介"'
    )

class RestPasswordSerializer(serializers.Serializer):
    """
    重置序列化参数
    """
    username = serializers.CharField(
        label=_("用户名"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    password = serializers.CharField(
        label=_("密码"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        allow_blank=False,
        write_only=True
    )
    phone = serializers.CharField(
        label=_("手机号"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    verify_code = serializers.CharField(
        label=_("验证码"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )


class GetTokenSerializer(serializers.Serializer):
    """
    get token api 序列化参数
    """

    username = serializers.CharField(
        label=_("用户名"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    password = serializers.CharField(
        label=_("密码"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        allow_blank=False,
        write_only=True
    )

class UpdateOwnerInfoSerializer(serializers.Serializer):
    """
    更新业主 序列化
    """
    organization_code = serializers.CharField(
        label=_("组织机构代码"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    organization_name = serializers.CharField(
        label=_("组织机构名称"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    corporation = serializers.CharField(
        label=_("法人"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    id_card_number = serializers.CharField(
        label=_("法人身份证"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    organization_picture = serializers.CharField(
        label=_("组织机构资质证明图片"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )

class AddProject(serializers.Serializer):
    """
    创建项目 序列化
    """
    project_name = serializers.CharField(
        label=_("项目名称"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )

    contract_person = serializers.CharField(
        label=_("联系人"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    contract_phone = serializers.CharField(
        label=_("联系人"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    project_scale = serializers.IntegerField(
        label=_("项目规模"),
    )
    project_limit = serializers.IntegerField(
        label=_("项目时限"),
    )
    service_low_count = serializers.FloatField(
        label=_("服务金额下限"),
    )
    service_high_count = serializers.FloatField(
        label=_("服务金额上限"),
    )
    content = serializers.CharField(
        label=_("服务内容"),
        allow_blank=True,
        write_only=True,
        trim_whitespace=True,
    )
    server_type = serializers.ListField(
        label=_('服务类型')
    )

    choice_type = serializers.ChoiceField(
        label=_("选取方式"),
        choices=("0", "1", "2", "3"),
    )
    begin_time = serializers.DateTimeField(
        label=_("开始时间"),
    )
    finish_time = serializers.DateTimeField(
        label=_("竞标终止时间"),
    )
    qualification = serializers.ChoiceField(
        label=_("资质要求"),
        choices=['0', '1', '2', '3']
    )
    remark = serializers.CharField(
        label=_("其他要求"),
        allow_blank=True,
        write_only=True,
        trim_whitespace=True,
    )
    file_url = serializers.ListField(
        label=_("上传文件"),
    )

class BidProjectSerializer(serializers.Serializer):
    """
    竞标项目 序列化
    """
    bid_money = serializers.IntegerField(
        label=_("竞标金额"),
    )
    describe = serializers.CharField(
        label=_("竞标描述"),
    )
    files_info = serializers.JSONField(
        label=_('文件'),
        help_text='格式{"file":"文件-选填", "text": "文本-选填"}',
        required=False,
    )

class ProjectListSerializer(serializers.Serializer):
    CHOICE_TYPE = (
        ("0", "择优选取"),
        ("1", "竞价选取"),
        ("2", "平均价选取"),
        ("3", "三次交互选取"),
    )
    QUERY_TYPE = (
        (0, "采购公告"),
        (1, "中选公告"),
        (2, "有合同的项目")
    )

    query_type = serializers.ChoiceField(
        label=_('查询模块数据'),
        choices=QUERY_TYPE,
        help_text='说明: 0:采购公告，1:中选公告 2: 过滤有合同的项目',
        required=False,
    )
    server_type = serializers.ListField(
        label=_('服务类型'),
        help_text='格式:[1,2,3]',
        required=False,
    )
    project_name = serializers.CharField(
        label=_("项目名称"),
        required=False,
    )
    choice_type = serializers.ChoiceField(
        label=_('选取方式'),
        choices=CHOICE_TYPE,
        required=False,
        help_text='"0":择优选取,"1":"竞价选取", "2":"平均价选取", "3":"三次交互选取"'
    )
    proprietor_name = serializers.CharField(
        label=_('业主名称'),
        required=False,
    )
    has_bid_project = serializers.ChoiceField(
        label=_('过滤参与竞标的项目'),
        choices=[0, 1],
        help_text='1:过滤参与的竞标项目',
        required=False,
    )
    offset = serializers.IntegerField(
        label=_("偏移量"),
        required=False,
    )
    limit = serializers.IntegerField(
        label=_("显示条数"),
        required=False,
    )



class CompanyListSerializer(serializers.Serializer):
    """
    中介列表
    """
    company_name = serializers.CharField(
        label=_("公司名称"),
        required=False,
        help_text='查询参数选填'
    )
    service_type = serializers.ListField(
        label=_("服务类型"),
        required=False,
        help_text='格式[1,2,4]'
    )
    rate_start = serializers.FloatField(
        label=_('星级评价'),
        required=False,

    )
    rate_end = serializers.FloatField(
        label=_('星级评价'),
        required=False,
    )

    offset = serializers.IntegerField(
        label=_("偏移量"),
    )
    limit = serializers.IntegerField(
        label=_("显示条数"),
    )

class SelectBidCompany(serializers.Serializer):
    """
    业主选标
    """
    project_id = serializers.CharField(
        label=_('项目ID'),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    intermediary_id = serializers.CharField(
        label=_('中介机构ID'),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,

    )

class SendMessageSerializer(serializers.Serializer):
    """
    发送短信列表
    """
    phone = serializers.CharField(
        label=_("手机号"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )


class UpdateCompanySeriallizer(serializers.Serializer):
    """
    中介信息
    """

    organization_code = serializers.CharField(
        label=_("统一社会信用代码/组织机构代码"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    organization_name = serializers.CharField(
        label=_("组织机构名称"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    corporation = serializers.CharField(
        label=_("法人"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    service_type = serializers.ListField(
        label=_('服务类型')
    )
    service_content = serializers.CharField(
        label=_("服务事项"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    address = serializers.CharField(
        label=_("公司地址"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    is_union = serializers.CharField(
        label=_("是否联合体"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    id_card_front_url = serializers.CharField(
        label=_("法人身份证正面"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    id_card_back_url = serializers.CharField(
        label=_("法人身份证被面"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    remark = serializers.CharField(
        label=_("备注"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    contract_person = serializers.CharField(
        label=_("联系人"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    co_id_card_front_url = serializers.CharField(
        label=_("联系人身份证国徽面"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    co_id_card_back_url = serializers.CharField(
        label=_("联系人身份证人像面"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    authorize_url = serializers.CharField(
        label=_("授权书"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    qualification_info = serializers.CharField(
        label=_("资质说明"),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )

    class QInner(serializers.Serializer):
        name = serializers.CharField(
            label=_("资质说明"),
            allow_blank=False,
            write_only=True,
            trim_whitespace=False,
        )
        url = serializers.CharField(
            label=_("资质图片路径"),
            allow_blank=False,
            write_only=True,
            trim_whitespace=False,
        )
    qualification_list = QInner(many=True)
    status = serializers.ChoiceField(
        label=_('状态'),
        choices=['0', '1']
    )
    enterprise_type = serializers.ChoiceField(
        label=_('企业类型'),
        choices=['0', '1', '2', '3']
    )


class ActiveSeriallizer(serializers.Serializer):
    """
    互动信息
    """
    intermediary_id = serializers.CharField(
        label=_('中介ID'),
        required=True
    )
    owner_response = serializers.CharField(
        label=_('回复内容'),
        required=True
    )


class ActiveListSeriallizer(serializers.Serializer):
    """
    互动信息
    """

    project_id = serializers.CharField(
        label=_('项目ID'),
        allow_blank=True,
        write_only=True,
        trim_whitespace=True,
    )
    project_name = serializers.CharField(
        label=_('项目名称'),
        allow_blank=True,
        write_only=True,
        trim_whitespace=True,
    )


class ServerTypeSeriallizer(openapi.Parameter):
    """
    服务类型
    """
    section_id = serializers.CharField(
        label=_('部门ID'),
        allow_blank=True,
        write_only=True,
        trim_whitespace=True,
    )
    section_name = serializers.CharField(
        label=_('部门名称'),
        allow_blank=True,
        write_only=True,
        trim_whitespace=True,
    )
    server_name = serializers.CharField(
        label=_('服务名称'),
        allow_blank=True,
        write_only=True,
        trim_whitespace=True,
    )


class SectionTypeSeriallizer(serializers.Serializer):
    """
    服务类型
    """
    section_id = serializers.CharField(
        label=_('部门ID'),
        allow_blank=True,
        write_only=True,
        trim_whitespace=True,
    )
    section_name = serializers.CharField(
        label=_('部门名称'),
        allow_blank=True,
        write_only=True,
        trim_whitespace=True,
    )


class BidPorjectListSerializer(serializers.Serializer):

    project_name = serializers.CharField(
        label=_("项目名称"),
        required=False,
        help_text='搜索条件选填'
    )
    proprietor_name = serializers.CharField(
        label=_('业主名称'),
        required=False,
        help_text='搜索条件选填'
    )
    offset = serializers.IntegerField(
        label=_("偏移量"),
    )
    limit = serializers.IntegerField(
        label=_("显示条数"),
    )


class ScoreCompanySerializer(serializers.Serializer):
    """
    评分
    """
    project_id = serializers.CharField(
        label=_('项目ID'),
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
    )
    score_level_one = serializers.IntegerField(
        label=_("一级评价"),
    )
    score_level_two = serializers.IntegerField(
        label=_("一级评价"),
    )
    score_level_three = serializers.IntegerField(
        label=_("一级评价"),
    )
    score_level_four = serializers.IntegerField(
        label=_("一级评价"),
    )
    score_level_five = serializers.IntegerField(
        label=_("一级评价"),
    )


class BidProjectListSerializer(serializers.Serializer):
    project_name = serializers.CharField(
        label=_("项目名称"),
        help_text='查询参数选填'
    )
    status = serializers.ChoiceField(
        label=_('状态'),
        choices=['0', '1'],
        help_text='"0":"未中标","1":"中标"'
    )
    offset = serializers.IntegerField(
        label=_("偏移量"),
    )
    limit = serializers.IntegerField(
        label=_("显示条数"),
    )