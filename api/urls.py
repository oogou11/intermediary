"""
API模块：提供给前端的业务接口
"""
from django.urls import path
from . import task
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('code/info/', views.code_data),  # 状态码说明
    path('token/', views.get_token),  # 获取用户token
    path('refresh/token/', views.get_token),  # 刷新token
    path('register/', views.register),  # 注册用户
    path('upload/', views.upload),  # 文件上传
    path('download/', views.download),  # 获取文件
    path('send_message/', views.send_message),  # 短信验证


    path('profile/detail/', views.profile_info),  # 用户基本详情
    path('profile/edit/', views.profile_edit),   # 更新用户基本信息
    path('rest/password/', views.reset_password),  # 重置密码


    path('user/owner/update/', views.update_owner_info),  # 完善业主信息
    path('owner/detail/', views.owner_detail),  # 业主详情
    path('owner/select/bid/company/', views.select_bid_company),  # 业主选标
    path('owner/view/bid/detail/<str:intermediary_id>/', views.owner_view_bid_detail),  # 业主查看竞标详情
    path('project/list/', views.project_list),  # 项目列表
    path('project/add/', views.create_project),  # 业主创建项目
    path('project/detail/<str:project_id>/', views.project_detail),  # 项目详情
    path('project/edit/<str:project_id>/', views.project_edit),  # 编辑项目
    path('owner/score/bid/company/',  views.score_company),  # 业主评价竞标公司


    path('user/company/update/', views.update_company_info),  # 完善中介信息
    path('company/detail/', views.company_detail),  # 中介详情
    path('list/bid/project/', views.bid_project_list),  # 竞标项目列表
    path('bid/project/<str:project_id>/', views.bid_project),  # 竞标
    path('bid/detail/<str:project_id>/', views.bid_detail),  # 竞标详情
    path('company/list/', views.company_list),  # 中介列表
    path('company/bid/project/list/', views.company_bid_projects),  # 中介参与的项目竞标
    path('response/bid/company/', views.response_medium),  # 回复竞标中介信息

    path('test/task/<str:project_id>/', views.test_task)
]

urlpatterns += router.urls
