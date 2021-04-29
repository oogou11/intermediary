"""
API模块：提供给前端的业务接口
"""
from django.urls import path
from . import views

urlpatterns = [
    path('project/list/', views.project_list),  # 项目列表
    path('service/type/', views.service_type),  # 项目类型
    path('section/type/', views.section_type),  # 部门类型
    path('company/list/', views.company_list),  # 中介列表
    path('project/detail/<str:project_id>/', views.project_detail),  # 项目详情
    path('aggregate/data/', views.get_aggregate_data),  # 统计业主、中介、项目总量
]
