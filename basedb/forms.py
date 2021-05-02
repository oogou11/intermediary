from django import forms
from .models import *


class SeverTypeAdmin(forms.ModelForm):
    """
    服务类型
    """
    picture_url = forms.ImageField(label='图片')

    class Meta:
        models = ServeType
        fields = '__all__'


class AutoSuperUserAdminForm(forms.ModelForm):
    """
    超级管理员
    """

    class Meta:
        models = User
        fields = '__all__'


class AutoUserAdminForm(forms.ModelForm):
    """
    用户
    """
    email = forms.CharField(label='邮箱', required=False)
    contacts = forms.CharField(label='联系人姓名', required=False)

    class Meta:
        models = User
        fields = '__all__'


class AutoProjectAdminForm(forms.ModelForm):
    """
    项目
    """
    sys_info = forms.CharField(widget=forms.Textarea(attrs={'rows': '3', 'cols': '80'}),
                               label="系统信息:选标",
                               required=False)
    project_message = forms.CharField(widget=forms.Textarea(attrs={'rows': '3', 'cols': '80'}),
                                      label="系统信息:流标",
                                      required=False)

    class Meta:
        models = Project
        fields = ('status', 'project_name', 'contract_person',
                  'contract_phone', 'contract_phone', 'project_scale',
                  'funds_source', 'project_limit', 'service_low_count',
                  'service_high_count', 'content', 'choice_type',
                  'server_type', 'create_user', 'proprietor',
                  'create_time', 'begin_time', 'finish_time',
                  'qualification', 'remark',
                  'score_level_one', 'score_level_two', 'score_level_three',
                  'score_level_four', 'score_level_five', 'average_score',
                  'project_message', 'sys_info', 'equal_bid_company')


