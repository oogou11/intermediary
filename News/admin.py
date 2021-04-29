from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import *
from django.utils.text import capfirst
from django.conf import settings
from import_export.admin import ImportExportModelAdmin, ExportActionMixin, ImportMixin
from basedb.models import User
# 注册顺序排序


@admin.register(NewsClass)
class NewsClassAdmin(admin.ModelAdmin):

    list_display = ['id', "NewsClassName", "NewsClassId"]
    ordering = ['-NewsClassId']
    list_filter = ['NewsClassId']
    search_fields = ['NewsClassName']
    list_per_page = 100


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):

    list_display = ["id", 'NewsClass', "NewsTitle",  "create_time"]
    list_filter = ['NewsClass']
    # list_editable = ["NewsTitle", ]


@admin.register(SinglePage)
class SinglePageAdmin(admin.ModelAdmin):

    list_display = ["id", "code", "NewsTitle",  "create_time"]
    # list_editable = ["NewsTitle", ]
