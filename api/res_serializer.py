from drf_yasg import openapi
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from basedb.models import *


class ServerTypeSerializers(serializers.Serializer):
    """
    服务类型
    """
    server_type_id = serializers.IntegerField(label=_('服务类型ID'))
    server_type_picture_url = serializers.CharField(label=_('服务类型封面地址'))
    server_type_name = serializers.CharField(label=_('服务类型名称'))
    section_id = serializers.CharField(label=_('部门ID'))
    section_name = serializers.CharField(label=_('部门名称'))


class BidCompanSerializers(serializers.Serializer):
    """
    竞标公司
    """
    bid_id = serializers.CharField(label=_('竞标ID'))
    intermediary_id = serializers.CharField(label=_('竞标中介机构ID'))
    intermediary_name = serializers.CharField(label=_('竞标中介机构名称'))
    bid_describe = serializers.CharField(label=_('竞标描述'))
    bid_money = serializers.IntegerField(label=_('竞标金额'))
    status = serializers.CharField(label=_('竞标状态'), help_text='字符串数字')
    status_name = serializers.CharField(label=_('竞标状态名称'))


class ResAPIProjectList(serializers.Serializer):
    """
    项目列表接口
    """
    id = serializers.CharField(label=_('项目ID')),
    project_name = serializers.CharField(label=_('项目名称'))
    contract_person = serializers.CharField(label=_('联系人'))
    contract_phone = serializers.CharField(label=_('联系电话'))
    project_scale = serializers.IntegerField(label=_('项目规模'))
    service_high_count = serializers.IntegerField(label=_('金额上限'))
    service_low_count = serializers.IntegerField(label=_('金额下限'))
    choice_type = serializers.CharField(label=_('选标方式'), help_text='字符串数字')
    choice_type_name = serializers.CharField(label=_('选标方式名称'))
    content = serializers.CharField(label=_('项目内容'))
    qualification = serializers.CharField(label=_('资质要求'), help_text='字符串数字')
    qualification_name = serializers.CharField(label=_('资质要求名称'))
    begin_time = serializers.CharField(label=_('项目开始时间'), help_text='2021-04-30 06:14:00')
    finish_time = serializers.CharField(label=_('项目结束时间'), help_text='2021-04-30 06:14:00')
    project_limit = serializers.IntegerField(label=_('项目期限'))
    bid_company = BidCompanSerializers(many=True, help_text='竞标公司，多个')
    bid_company_count = serializers.IntegerField(label=_('竞标公司数量'))
    status = serializers.CharField(label=_('项目状态'), help_text='字符串数字')
    status_name = serializers.CharField(label=_('项目状态名称'))
    remark = serializers.CharField(label=_('其他要求'))
    file_url = serializers.ListField(label=_('文件地址'), help_text='资料附件:文件数组')
    contract = serializers.ListField(label=_('合同'), help_text='合同:文件数组')
    server_type = ServerTypeSerializers(many=True)


class BaseAPIProjectList(serializers.Serializer):
    """
    项目列表
    """

    code = serializers.IntegerField(
        label=_('返回状态吗'),
        help_text='成功是200,非200参考业务码接口'
    )
    msg = serializers.CharField(
        label=_('信息提示')
    )
    data = ResAPIProjectList(many=True)


class ResBidDetailSerializers(serializers.Serializer):
    """竞标详情"""

    class BidDetailSerializers(serializers.Serializer):
        """
        竞标详情字段
        """
        id = serializers.CharField(label=_('竞标ID'))
        project_id = serializers.CharField(label=_('项目ID'))
        project_name = serializers.CharField(label=_('项目名称'))
        bid_money = serializers.IntegerField(label=_('竞标金额'))
        files_info = serializers.ListField(label=_('附件信息'), help_text='竞标时上传的文件')
        describe = serializers.CharField(label=_('竞标描述'))
        create_time = serializers.CharField(label=_('竞标时间'), help_text='2021-04-30 15:20:57')
        update_time = serializers.CharField(label=_('更细时间'), help_text='2021-04-30 15:20:57')
        status = serializers.CharField(label=_('竞标状态'))
        status_name = serializers.CharField(label=_('状态名称'))
        owner_response = serializers.ListField(label='业主回复')
    code = serializers.IntegerField(
        label=_('返回状态吗'),
        help_text='成功是200,非200参考业务码接口'
    )
    msg = serializers.CharField(
        label=_('信息提示')
    )
    data = BidDetailSerializers(many=True)

class ResOwnerViewBidDetailSerializer(serializers.Serializer):
    """
    业主查看竞标详情
    """
    class OwnerBidDetailSerializers(serializers.Serializer):
        """
        竞标详情字段
        """
        id = serializers.CharField(label=_('竞标ID'))
        project_id = serializers.CharField(label=_('项目ID'))
        project_name = serializers.CharField(label=_('项目名称'))
        bid_money = serializers.IntegerField(label=_('竞标金额'))
        files_info = serializers.ListField(label=_('附件信息'), help_text='竞标时上传的文件')
        describe = serializers.CharField(label=_('竞标描述'))
        create_time = serializers.CharField(label=_('竞标时间'), help_text='2021-04-30 15:20:57')
        update_time = serializers.CharField(label=_('更细时间'), help_text='2021-04-30 15:20:57')
        status = serializers.CharField(label=_('竞标状态'))
        status_name = serializers.CharField(label=_('状态名称'))
        owner_response = serializers.ListField(label='业主回复')
    code = serializers.IntegerField(
        label=_('返回状态吗'),
        help_text='成功是200,非200参考业务码接口'
    )
    msg = serializers.CharField(
        label=_('信息提示')
    )
    data = OwnerBidDetailSerializers()


class ResCompanyBidProjectList(serializers.Serializer):
    class CompanyBidProjectList(serializers.Serializer):
        """
        竞标累表
        """
        id = serializers.CharField(label=_('竞标ID'))
        project_id = serializers.CharField(label=_('项目ID'))
        project_name = serializers.CharField(label=_('项目名称'))
        proprietor = serializers.CharField(label=_('业主名称'))
        create_time = serializers.CharField(label=_('创建时间'), help_text='2021-04-30 15:20:57')
        status = serializers.CharField(label=_('竞标状态'), help_text='字符串数字')
        status_name = serializers.CharField(label=_('竞标状态名称'))

    code = serializers.IntegerField(
        label=_('返回状态吗'),
        help_text='成功是200,非200参考业务码接口'
    )
    msg = serializers.CharField(
        label=_('信息提示')
    )
    count = serializers.IntegerField(label=_('总条数'))
    data = CompanyBidProjectList(many=True)


class ResCompanyDetail(serializers.Serializer):
    """
    公司详情
    """
    intermediary_id = serializers.CharField(label=_('中介ID'))
    organization_code = serializers.CharField(label=_('统一社会信用代码/组织机构代码'))
    organization_name = serializers.CharField(label=_('组织机构名称'))
    corporation = serializers.CharField(label=_('法人'))
    service_type = ServerTypeSerializers(many=True, label='服务类型')
    enterprise_type = serializers.CharField(label=_('机构类型'), help_text='"0":"其他", "1":"社会","2":"事业单位", "3":"政府机构"')
    enterprise_type_name = serializers.CharField(label=_('机构类型名称'))
    service_content = serializers.CharField(label=_('服务事项'))
    address = serializers.CharField(label=_('公司地址'))
    is_union = serializers.BooleanField(label=_('是否联合体'))
    id_card_front_url = serializers.CharField(label=_('法人身份证正面'))
    id_card_back_url = serializers.CharField(label=_('法人身份证被面'))
    remark = serializers.CharField(label=_('备注'), required=False)
    contract_person = serializers.CharField(label=_('联系人'))
    co_id_card_front_url = serializers.CharField(label=_('联系人身份证正面'), required=False)
    co_id_card_back_url = serializers.CharField(label=_('联系人身份证背面'), required=False)
    authorize_url = serializers.CharField(label=_('授权书'), required=False)
    qualification_info = serializers.CharField(label=_('资质说明'), required=False)
    qualification_list = serializers.ListField(help_text='[{"name": "资质名称", "url": "资质图片"}]')
    status = serializers.CharField(label=_('状态'), help_text='"0:-保存草稿，"1"："提交审核中"')
    status_name = serializers.CharField(label=_('状态名称'))


class ResCompaynListSerializer(serializers.Serializer):
    code = serializers.IntegerField(
        label=_('返回状态吗'),
        help_text='成功是200,非200参考业务码接口'
    )
    msg = serializers.CharField(
        label=_('信息提示')
    )
    count = serializers.IntegerField(label=_('总条数'))
    data = ResCompanyDetail(many=True)


class ResOwnerDetailSerializer(serializers.Serializer):
    """
    业主
    """
    class OwnerDetailSerializer(serializers.Serializer):
        business_id = serializers.IntegerField(label=_('主键'))
        organization_code = serializers.CharField(label=_('统一社会信用代码/组织机构代码'))
        organization_name = serializers.CharField(label=_('组织机构名称'))
        corporation = serializers.CharField(label=_('法人'))
        id_card_number = serializers.CharField(label=_('身份证号'))
        organization_picture = serializers.ListField(label=_('文件'), help_text='格式["url", "url]'),
        status = serializers.CharField(label=_('状态'), help_text='"0:-保存草稿，"1"："提交审核中"')
        status_name = serializers.CharField(label=_('状态名称'))
        create_time = serializers.CharField(label=_('竞标时间'), help_text='2021-04-30 15:20:57')

    code = serializers.IntegerField(
        label=_('返回状态吗'),
        help_text='成功是200,非200参考业务码接口'
    )
    msg = serializers.CharField(
        label=_('信息提示')
    )
    data = ResCompanyDetail()


class ResUserProfileSerializer(serializers.Serializer):
    class UserProfileSerializer(serializers.Serializer):
        username = serializers.CharField(label=_('用户名'))
        customer_type = serializers.CharField(label=_('用户类型'))
        phone = serializers.CharField(label=_('注册电话'))
        email = serializers.CharField(label=_('注册邮箱'))

    code = serializers.IntegerField(
        label=_('返回状态吗'),
        help_text='成功是200,非200参考业务码接口'
    )
    msg = serializers.CharField(
        label=_('信息提示')
    )
    data = UserProfileSerializer()



class ResProjectDetail(serializers.Serializer):
    """
    项目详情
    """
    code = serializers.IntegerField(
        label=_('返回状态吗'),
        help_text='成功是200,非200参考业务码接口'
    )
    msg = serializers.CharField(
        label=_('信息提示')
    )
    data = ResAPIProjectList()


class ResTokenSerializer(serializers.Serializer):
    class TokenSerializer(serializers.Serializer):
        """
        token
        """
        token = serializers.CharField(label=_('token值'))
        user_id = serializers.CharField(label=_('用户ID'))
        username = serializers.CharField(label=_('用户名'))
        phone = serializers.CharField(label=_('电话'))
        email = serializers.CharField(label=_('邮箱'))
        company_name = serializers.CharField(label=_('所在单位'))
        role = serializers.CharField(label=_('角色'), help_text='字符串数字: 1-业主 2-中介')
        status = serializers.CharField(label=_('用户状态'), help_text='字符串数字')
        status_name = serializers.CharField(label=_('状态描述'))

    code = serializers.IntegerField(
        label=_('返回状态吗'),
        help_text='成功是200,非200参考业务码接口'
    )
    msg = serializers.CharField(
        label=_('信息提示')
    )
    data = TokenSerializer()


token_response = openapi.Response('返回格式', ResTokenSerializer)
project_detail_response = openapi.Response('返回格式', ResProjectDetail)
user_profile_response = openapi.Response('返回格式', ResUserProfileSerializer)
owner_detail_response = openapi.Response('返回格式', ResOwnerDetailSerializer)
company_list_response = openapi.Response('返回格式', ResCompaynListSerializer)
company_detail_response = openapi.Response('返回格式', ResCompanyDetail)
company_bid_list_response = openapi.Response('返回格式', ResCompanyBidProjectList)
bid_detail_response = openapi.Response('返回格式', ResBidDetailSerializers)
owner_view_bid_detail_response = openapi.Response('返回格式', ResOwnerViewBidDetailSerializer)
project_list_response = openapi.Response('返回格式', BaseAPIProjectList)



