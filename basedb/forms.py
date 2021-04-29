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
    sys_info_area = forms.Textarea()
    project_message_area = forms.Textarea()

    class Meta:
        models = Project
        fields = '__all__'


