import datetime
import os
import uuid
from django.contrib import admin
from django.contrib.auth.password_validation import password_changed
from .models import *
from django.conf import settings
from django.utils.text import capfirst
from django.utils.safestring import mark_safe
from .forms import *
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy


admin.site.unregister(Group)  # 菜单不显示用户组
admin.site.unregister(TokenProxy)  # 菜单不显示授权认证

def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        templateresponse = func(*args, **kwargs)
        for app in templateresponse.context_data['app_list']:
            if app.get('app_label') == 'basedb':
                app.update({'name': '系统管理'})
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return templateresponse
    return inner


registry = dict()
registry.update(admin.site._registry)
admin.site._registry = registry
admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)
admin.AdminSite.site_header = settings.BASESET["title"]
admin.AdminSite.site_title = settings.BASESET["title"]


def upload_file(file, role=None):
    origin_name = file.name
    relative_path = '{}_{}/'.format('admin', 'server_type')
    folder_path = '{}/{}'.format(settings.UPLOADFILES_DIRS, relative_path)
    file_type = file.content_type.split('/')[-1]
    # 路径不存在创建路径
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    new_file_name = '{}.{}'.format(str(uuid.uuid1()), file_type)
    full_filename = os.path.join(folder_path, new_file_name)
    pic_data = open(full_filename, 'wb+')
    for chunk in file.chunks():
        pic_data.write(chunk)
    pic_data.close()
    url = 'api/download?url=' + relative_path + new_file_name
    if role is not None:
        url += '&role=2'
    return origin_name, settings.DOMAIN_HOST + url


@admin.register(ServeType)
class ServeTypeAdmin(admin.ModelAdmin):
    form = SeverTypeAdmin
    list_display = ('server_name', 'section_id')
    list_filter = ('server_name',)
    readonly_fields = ('picture_show',)
    search_fields = ('server_name', 'section_id__section_name')

    def picture_show(self, obj):
        """
        证件图片
        :param obj:
        :return:
        """
        if obj.picture_url is not None:
            return mark_safe('<img src="{url}" width="400px" height="400px" /> '.format(
                url='/static/files/' + obj.picture_url.split('url=')[1].split('&')[0]
            )
            )
        else:
            return '无'

    picture_show.short_description = '图片展示'

    def save_model(self, request, obj, form, change):
        """
        :param reqeust:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        url = ''
        if form.files:
            file = form.files.get('picture_url')
            origin_name, url = upload_file(file, '2')
        obj.picture_url = url
        super().save_model(request, obj, form, change)


@admin.register(SectionType)
class SectionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'section_name')
    list_filter = ('section_name',)

    search_fields = ('section_name', )


class ProprietorProfileIn(admin.StackedInline):
    """
    业主
    """

    model = ProprietorProfile
    extra = 0
    fields = ('status', 'organization_name', 'organization_code', 'corporation',
              'id_card_number', 'create_time',
              'update_time', 'picture_show')

    readonly_fields = ['picture_show']

    def picture_show(self, obj):
        """
        证件图片
        :param obj:
        :return:
        """
        if obj.organization_picture is not None:
            file_url = ''
            prefix = '/static/files/'
            for p in obj.organization_picture:
                path_url = p.split('url=')[1].split('&')[0]
                backend_prefix = path_url.split('.')[1]
                if backend_prefix in ('jpg', 'jpeg', 'JPG', 'JPEG', 'png', 'PNG'):
                    file_url += '<img src="{}" width="400px" height="400px" />'.format(
                         prefix + p.split('url=')[1].split('&')[0]
                    )
                else:
                    file_url += '<a href="{}"/>'.format(
                        prefix + path_url
                    )
            return mark_safe(file_url)
        else:
            return '无'

    picture_show.short_description = '资料展示'


class IntermediaryProfileIn(admin.StackedInline):
    """
    中介
    """
    model = IntermediaryProfile
    extra = 0
    fields = ('status', 'organization_name', 'organization_code', 'corporation',
              'service_type', 'service_content', 'address', 'is_union',
              'id_card_front_url', 'id_card_back_url', 'remark',
              'contract_person', 'co_id_card_front_url', 'co_id_card_back_url',
              'authorize_url', 'qualification_info', 'super_rate', 'qualification_list',
              'qualification_file_list',
              'update_time')
    readonly_fields = ['qualification_file_list']

    def qualification_file_list(self, obj):
        """
        证件图片
        :param obj:
        :return:
        """
        if obj.qualification_list is not None:
            if isinstance(obj.qualification_list, list) and len(obj.qualification_list) == 0:
                return '无'
            file_url = ''
            prefix = '/static/files/'
            for p in obj.qualification_list:
                p_url = p.get('url', '')
                if 'url=' not in p_url:
                    continue
                path_url = p_url.split('url=')[1].split('&')[0]
                backend_prefix = path_url.split('.')[1]
                if backend_prefix in ('jpg', 'jpeg', 'JPG', 'JPEG', 'png', 'PNG'):
                    file_url += '<label>{}</label>' \
                                '<img src="{}" width="400px" height="400px" />'.format(
                        p.get('name'), prefix + path_url
                    )
                else:
                    file_url += '</br>'
                    file_url += '<a href="{}">{}</a>'.format(prefix + path_url, p.get('name')
                    )
            return mark_safe(file_url)
        else:
            return '无'

    qualification_file_list.short_description = '资料展示'


class SuperUserModel(User):

    class Meta:
        verbose_name = "超级管理员"
        verbose_name_plural = verbose_name
        proxy = True


class SuperUserAdmin(admin.ModelAdmin):
    """
    超级管理员
    """

    list_display = ('username', 'phone', 'email',)

    def get_queryset(self, request):
        """
        用户只显示：只展示超级管理员
        :param request:
        :return:
        """
        qs = super().get_queryset(request)
        return qs.filter(customer_type='0')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        重写编辑页面
        :param request:
        :param object_id:
        :param extra_context:
        :return:
        """
        self.fields = ("username", "password", "email")
        self.readonly_fields = ("username", "email")
        return super(SuperUserAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        """
        更改密码
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        if change:
            user = User.objects.get(username=obj.username)
            user.set_password(obj.password)
            user.save()
        else:
            super().save_model(request, obj, form, change)


admin.site.register(SuperUserModel, SuperUserAdmin)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    form = AutoUserAdminForm

    list_display = ('username', 'contacts', 'customer_type', 'statustype',
                    'phone', 'is_active', 'rate',)
    list_display_links = ['username', 'contacts', ]
    list_filter = ('customer_type', 'statustype', 'is_active',)

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')
    list_per_page = 100
    inlines = [ProprietorProfileIn, IntermediaryProfileIn]


    def get_queryset(self, request):
        """
        用户只显示：业主和中介
        :param request:
        :return:
        """
        qs = super().get_queryset(request)
        return qs.filter(customer_type__in=['1', '2'])

    def get_inlines(self, request, obj):
        """Hook for specifying custom inlines."""
        print(request, obj.customer_type)
        if obj.customer_type == '1':
            return [ProprietorProfileIn, ]
        if obj.customer_type == '2':
            return [IntermediaryProfileIn, ]
        return []

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        重写编辑页面
        :param request:
        :param object_id:
        :param extra_context:
        :return:
        """
        self.fields = ("statustype", "username", "phone", "email",
                       "contacts",)
        self.readonly_fields = ("username",)
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    中介审核 template model
    """
    form = AutoProjectAdminForm
    list_display = ('id', 'project_name')
    search_fields = ('project_name', )
    list_per_page = 100
    def file_url_list(self, obj):
        """
        证件图片
        :param obj:
        :return:
        """
        if obj.file_url is not None:
            if isinstance(obj.file_url, list) and len(obj.file_url) == 0:
                return '无'
            file_url = ''
            prefix = '/static/files/'
            for p in obj.file_url:
                p_url = p.get('url')
                path_url = p_url.split('url=')[1].split('&')[0]
                backend_prefix = path_url.split('.')[1]
                if backend_prefix in ('jpg', 'jpeg', 'JPG', 'JPEG', 'png', 'PNG'):
                    file_url += '<label>{}</label>' \
                                '<img src="{}" width="400px" height="400px" />'.format(
                        p.get('name'), prefix + path_url
                    )
                else:
                    file_url += '</br>'
                    file_url += '<a href="{}">{}</a>'.format(prefix + path_url, p.get('name')
                                                             )
            return mark_safe(file_url)
        else:
            return '无'

    def contract_list(self, obj):
        """
        证件图片
        :param obj:
        :return:
        """
        if obj.contract is not None:
            file_url = ''
            prefix = '/static/files/'
            for p in obj.contract:
                p_url = p.get('url')
                path_url = p_url.split('url=')[1].split('&')[0]
                backend_prefix = path_url.split('.')[1]
                if backend_prefix in ('jpg', 'jpeg', 'JPG', 'JPEG', 'png', 'PNG'):
                    file_url += '<label>{}</label>' \
                                '<img src="{}" width="400px" height="400px" />'.format(
                        p.get('name'), prefix + path_url
                    )
                else:
                    file_url += '</br>'
                    file_url += '<a href="{}">{}</a>'.format(prefix + path_url, p.get('name')
                                                             )
            return mark_safe(file_url)
        else:
            return '无'

    def save_model(self, reqeust, obj, form, change):
        """
        :param reqeust:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        file_files = reqeust.FILES.getlist('file_url_address')  # 上传文件
        contract_files = reqeust.FILES.getlist('contract_address')  # 合同
        if len(file_files) > 0:
            file_url = list()
            for file in file_files:
                origin_name, url = upload_file(file, '2')
                file_url.append({'name': origin_name, 'url': url})
            obj.file_url = file_url

        if len(contract_files) > 0:
            contract_url = list()
            for file in contract_files:
                origin_name, url = upload_file(file, '2')
                contract_url.append({'name': origin_name, 'url': url})
            obj.contract = contract_url
        obj.save()


@admin.register(BidProject)
class BidProjectAdmin(admin.ModelAdmin):
    """
    竞标
    """
    list_display = ('id', 'project')
    list_per_page = 100