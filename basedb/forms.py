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
    file_url_address = forms.FileField(required=False,
                                       widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                       label='上传文件admin操作')
    contract_address = forms.FileField(required=False,
                                       widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                       label='合同admin操作')
    sys_info = forms.CharField(widget=forms.Textarea(attrs={'rows': '3', 'cols': '80'}),
                               label="系统信息:选标",
                               required=False)
    project_message = forms.CharField(widget=forms.Textarea(attrs={'rows': '3', 'cols': '80'}),
                                      label="系统信息:流标",
                                      required=False)

    class Meta:
        models = Project
        fields = '__all__'


