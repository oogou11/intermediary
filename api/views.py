"""
业务API模块: token验证，项目竞标流程等
"""
import os
import uuid
import json
import gevent
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.http import FileResponse
from .service import UserService, AuditService, ProjectService, SendMessagServie
from .service import ServiceTypeService
from .task import CoreTasks
from .serializer import *
from utils.code import response, authorize, code_info
from django.views.decorators.csrf import csrf_exempt
from .send_message import *
from .res_serializer import *


@csrf_exempt
@api_view(['GET'])
def code_data(request):
    """
    接口code码说明
    """
    return Response(code_info)


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=GetTokenSerializer,
                     responses={'200': token_response})
@api_view(['POST'])
@response
def get_token(request):
    """
    获取用户token
    """
    params = json.loads(request.body)
    username = params.get('username')
    password = params.get('password')
    service = UserService()
    user = service.get_user_by_username_and_password(username, password)
    if user is None:
        return {'code': 20001}
    else:
        if user.user_token.first() is not None:
            token_data = service.update_toke(user)
        else:
            token_data = service.create_token(user)
        if user.customer_type == '1':
            company_name = user.proprietor_user.first().organization_name if user.proprietor_user.first() else ''
        elif user.customer_type == '2':
            company_name = user.user_company.first().organization_name if user.user_company.first() else ''
        else:
            company_name = ''
        return {'code': 200, 'data': {'token': token_data,
                                      'user_id': user.id,
                                      'username': user.username,
                                      'phone': user.phone,
                                      'email': user.email,
                                      'company_name': company_name,
                                      'role': user.customer_type,
                                      'status': user.statustype,
                                      'status_name': user.get_status_name}}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=RegisterSerializer,
                     responses={200: ''})
@api_view(['POST'])
@response
def register(request):

    params = json.loads(request.body)
    username = params.get('username', None)  # 用户名
    password = params.get('password', None)  # 密码
    phone = params.get('phone', None)  # 手机号
    email = params.get('email', None)  # 邮箱
    verify_code = params.get('verify_code', None)
    customer_type = params.get('customer_type', None)  # 用户类型
    if username is None or len(username) == 0:
        return {'code': 20010}
    if password is None or len(password) == 0:
        return {'code': 20012}
    if email is None or len(email) == 0:
        return {'code': 20013}
    if phone is None or len(phone) == 0:
        return {'code': 20014}
    if customer_type is None:
        return {'code': 20015}
    if customer_type not in ('0', '1', '2'):
        return {'code': 20016}
    if verify_code is None or len(verify_code) == 0:
        return {'code': 20020}
    service = UserService()
    # 验证验证码的有效性
    can_be_passed = service.check_phone_code(phone, verify_code)
    if not can_be_passed:
        return {'code': 20020}
    is_exist = service.get_user_by_username(username)
    if is_exist is not None:
        return {'code': 20017}
    service.create_user(username, password,  phone, email, customer_type)
    return {'code': 200}


@csrf_exempt
@swagger_auto_schema(methods=['get'],  responses={'200': user_profile_response})
@api_view(['GET'])
@authorize
@response
def profile_info(request):
    """
    用户基本详情

    """
    data = UserService().get_user_by_id_to_dict(request.user.id)
    return {'code': 200, 'data': data}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=RegisterSerializer,
                     responses={200: ''})
@api_view(['POST'])
@response
def profile_edit(request):
    """
    用户基本详情
    """
    if request.body is None:
        return {'code': 10103}
    params = json.loads(request.body)
    phone = params.get('phone', None)  # 手机号
    email = params.get('email', None)  # 邮箱
    if phone != request.user.phone:
        verify_code = params.get('verify_code', None)
        service = UserService()
        # 验证验证码的有效性
        can_be_passed = service.check_phone_code(phone, verify_code)
        if not can_be_passed:
            return {'code': 20020}
    UserService().update(request.user.id, {'username': params.get('username'),
                                           'phone': phone,
                                           'email': email})
    return {'code': 200}



@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=RestPasswordSerializer,
                     responses={200: ''})
@api_view(['POST'])
@response
def reset_password(request):
    """
    重置密码
    """
    params = json.loads(request.body)
    username = params.get('username', None)  # 用户名
    password = params.get('password', None)  # 密码
    phone = params.get('phone', None)  # 手机号
    verify_code = params.get('verify_code', None)
    if username is None or len(username) == 0:
        return {'code': 20010}
    if password is None or len(password) == 0:
        return {'code': 20012}
    if phone is None or len(phone) == 0:
        return {'code': 20014}
    service = UserService()
    # 验证验证码的有效性
    can_be_passed = service.check_phone_code(phone, verify_code)
    if not can_be_passed:
        return {'code': 20020}
    is_exist_data = service.reset_password(username, phone, password)
    if not is_exist_data:
        return {'code': 20017}
    return {'code': 200}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=UpdateOwnerInfoSerializer,
                     responses={200: ''})
@api_view(['POST'])
@authorize
@response
def update_owner_info(request):
    """
    完善业主信息
    """
    if request.user.customer_type != '1':
        return {'code': 10109}
    data = json.loads(request.body)
    service = UserService()
    audit_service = AuditService()
    user = service.get_user_by_id(request.user.id)
    if user is None:
        return {'code': 10013}

    # 更新业主信息
    can_be_updated, owner = service.update_owner_info(user, data)
    if not can_be_updated:
        return {'code': 20018}
    # 更新用户状态--审核中
    audit_service.update_user_status(request.user.id)
    # 短信通知管理员
    if owner.status == '1':
        SendMessagServie().send_user_to_verify(1, owner.organization_name)
    return {'code': 200, 'data': {}}


@csrf_exempt
@swagger_auto_schema(methods=['get'],   responses={'200': owner_detail_response})
@api_view(['GET'])
@authorize
@response
def owner_detail(request):
    """
    业主详情
    接口会自动获取token中的业主信息。不需要传递参数
    """
    user = request.user
    if user.customer_type != '1':
        return {'code': 10109}

    data = UserService().owner_detail(user.id)
    return {'code': 200, 'data': data}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=SelectBidCompany,
                     responses={200: ''})
@api_view(['POST'])
@authorize
@response
def select_bid_company(request):
    """
    业主选标
    """
    if request.body is None:
        return {'code': 10103}
    params = json.loads(request.body)
    project_id = params.get('project_id', None)
    intermediary_id = params.get('intermediary_id', None)
    if project_id is None or intermediary_id is None:
        return {'code': 10103}
    is_selected, code_or_bid_info = ProjectService().select_bid_company(project_id, intermediary_id)
    if not is_selected:
        return {'code': code_or_bid_info}
    # 短信通知中标公司
    SendMessagServie().win_bind_msg(code_or_bid_info.bid_company, code_or_bid_info.project)
    return {'code': 200}


@csrf_exempt
@swagger_auto_schema(methods=['get'],   responses={'200': owner_view_bid_detail_response})
@api_view(['GET'])
@authorize
@response
def owner_view_bid_detail(request, intermediary_id, project_id):
    """
    业主查看竞标详情
    """
    if intermediary_id is None or project_id is None:
        return {'code': 10103}
    data = ProjectService().get_bid_detail_for_owner(intermediary_id, project_id)
    return {'code': 200, 'data': data}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=CompanyListSerializer,
                     responses={'200': company_list_response})
@api_view(['POST'])
@response
def company_list(request):
    """
    中介列表
    """
    body_info = request.body
    offset = '0'
    limit = '10'
    service_type = None
    company_name = None
    if body_info is not None:
        params = json.loads(body_info)
        offset = params.get('offset', '0')
        limit = params.get('limit', '10')
        company_name = params.get('company_name', None)
        service_type = params.get('service_type', None)
    if isinstance(offset, str):
        offset = int(offset)
    if isinstance(limit, str):
        limit = int(limit)
    total_count, data = UserService().get_company_list(service_type, company_name, offset, limit)
    return {'code': 200, "count": total_count, 'data': data}


@csrf_exempt
@swagger_auto_schema(methods=['get'],  responses={'200': company_detail_response})
@api_view(['GET'])
@authorize
@response
def company_detail(request):
    """
    中介详情
    """
    user = request.user
    if user.customer_type != '2':
        return {'code': 10109}
    data = UserService().company_detail(user.id)
    return {'code': 200, 'data': data}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=UpdateCompanySeriallizer,
                     responses={200: ''})
@api_view(['POST'])
@authorize
@response
def update_company_info(request):
    """
    完善中介信息
    """
    if request.user.customer_type != '2':
        return {'code': 10109}
    data = json.loads(request.body)
    service = UserService()
    audit_service = AuditService()
    user = service.get_user_by_id(request.user.id)
    if user is None:
        return {'code': 10013}

    can_be_updated, company = service.update_company_info(user, data)
    if not can_be_updated:
        return {'code': 20019}
    # # 更新用户状态--审核中
    if data.get('status') == '1':
        audit_service.update_user_status(request.user.id)
        # 短信通知管理员
        SendMessagServie().send_user_to_verify(2, company.organization_name)
    return {'code': 200, 'data': {}}


@csrf_exempt
@api_view(['POST'])
@authorize
@response
def upload(request):
    """
    文件上传
    说明: body的Media Type:为form-data格式。文件对应的key为file
    请求信息: {"file": "FILE Info"}
    返回结果:
    {
        "code": 200,
        "msg": "success",
        "data": {"url": "http:127.0.0.1:8090/api/download?url=static/files/abc.jpeg"}
    }
    """
    allow_file_type = ('jpg', 'png', 'gif', 'jpeg',
                       'pdf', 'zip', 'rar', '7z',
                       'doc', 'docx', 'xls', 'xlsx',
                       'ppt', 'pptx')
    # 用户名_用户ID，构成文件夹路径
    relative_path = '{}_{}/'.format(request.user.id, request.user.username)
    folder_path = '{}/{}'.format(settings.UPLOADFILES_DIRS, relative_path)
    # 路径不存在创建路径
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # 获取上传的文件
    file = request.FILES.get('file')  # 获取文件
    if file is None:
        return {'code': 10010}
    # 文件类型
    file_type = file.content_type.split('/')[-1]
    if file_type not in allow_file_type:
        return {'code': 10011}
    # 更改文件名
    new_file_name = '{}.{}'.format(str(uuid.uuid1()), file_type)
    full_filename = os.path.join(folder_path, new_file_name)
    pic_data = open(full_filename, 'wb+')
    for chunk in file.chunks():
        pic_data.write(chunk)
    pic_data.close()

    url = 'api/download?url=' + relative_path + new_file_name
    if request.user.customer_type == '2':
        """
        中介图片公开
        """
        url += '&role=2'
    return {'code': 200, 'data': {'host': settings.DOMAIN_HOST + url}}


@csrf_exempt
@api_view(['GET'])
@authorize
def download(request):
    """
    下载文件
    请求信息: http://host/api/download?url=static/files/user_folder/abc.jpeg
    返回结果: stream
    """
    file_url = request.GET.get('url')
    if file_url is None:
        return {'code': 10103, 'msg': '缺少必要参数'}
    file_path = '{}/{}'.format(settings.UPLOADFILES_DIRS, file_url)
    if not os.path.exists(file_path):
        return {'code': 10104, 'msg': '文件不存在!'}

    filename = file_url.split('/')[-1]
    down_file = open(file_path, 'rb')
    res = FileResponse(down_file)
    res['Content-Type'] = 'application/octet-stream'
    res['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
    return res


@csrf_exempt
@api_view(['POST'])
@authorize
@response
def admin_verify_info(request, id, verify_type):
    """
    管理员审核
    url格式:
    请求信息:
    返回结果:
    """
    if request.method == 'POST':
        if request.user.customer_type != '0':
            return {'code': 10109}
        params = json.loads(request.body)
        business_id = params.get('business_id')
        content = params.get('content', '')
        status = params.get('status', None)
        if status is None or len(status) == 0:
            return {'code': 10103}
        service = AuditService()
        user = request.user
        if verify_type == '0':  # 审核业主信息
            is_updated, owner = service.audit_owner(user, business_id, id, content, status)
            if is_updated:
                return {'code': 200}
        elif verify_type == '1':  # 审核中介信息
            is_updated, company = service.audit_company(user, business_id, id, content, status)
            if is_updated:
                return {'code': 200}
        elif verify_type == '2':  # 审核项目信息
            is_updated, project = service.audit_project(user, business_id, id, content, status)
            if is_updated:
                # 需要增加定时任务，时间到后自动根据规则进行选标
                gevent.spawn(CoreTasks().create_core_job(project))
                return {'code': 200}
        elif verify_type == '3':  # 审核答疑信息
            pass
        else:
            return {'code': 10105}
        return {'code': 10106}
    return {'code': 200}


@csrf_exempt
# @api_view(['GET'])
# @authorize
@response
def admin_service_type(request):
    """
    后台管理类型，需要登录
    请求信息:
    返回结果:
    {
        "code": 200,
        "msg": "success",
        "data": ["id": 1, "name": "工程管理", "chid": [ {"id": 121, "name": "管理"} ] ]
    }
    """
    data = ServiceTypeService().get_service_type_list()
    return {'code': 200, 'data': data}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=AddProject,
                     responses={200: ''})
@api_view(['POST'])
@authorize
@response
def create_project(request):
    """
    业主创建项目
    """
    user = request.user
    if user.customer_type != '1':  # 非业主不允许操纵
        return {'code': 10108}
    data = json.loads(request.body)
    project = ProjectService().create_project(request.user, data)
    if project.status == '1':
        # 短信通知管理员
        SendMessagServie().send_user_to_verify(3, project.proprietor.organization_name)
    return {'code': 200, 'data': {'project_id': project.id}}


@csrf_exempt
@swagger_auto_schema(methods=['get'], responses={'200': project_detail_response})
@api_view(['GET'])
@authorize
@response
def project_detail(request, project_id):
    """
    获取项目详情
    """
    if project_id is None:
        return {'code': 10103}
    data = ProjectService().get_project_by_id(project_id, is_owner=True)
    return {'code': 200, 'data': data}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=AddProject,
                     responses={200: ''})
@api_view(['POST'])
@authorize
@response
def project_edit(request, project_id):
    """
    编辑项目
    """
    if project_id is None:
        return {'code': 10103}
    if request.body is None:
        return {'code': 10103}
    data = json.loads(request.body)
    is_update, code_or_pro = ProjectService().update_project(request.user, project_id, data)
    if not is_update:
        return {'code': code_or_pro}
    if code_or_pro.status == '1':
        # 短信通知管理员
        SendMessagServie().send_user_to_verify(3, code_or_pro.proprietor.organization_name)
    return {'code': 200}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=ScoreCompanySerializer,
                     responses={200: ''})
@api_view(['POST'])
@authorize
@response
def score_company(request):
    """
    给中介打分
    :return:
    """
    params = json.loads(request.body)
    project_id = params.get('project_id', None)
    if project_id is None:
        return {'code': 10103}
    del params['project_id']
    ProjectService().score_company(project_id, params)
    return {'code': 200}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=BidProjectSerializer,
                     responses={200: ''})
@api_view(['POST'])
@authorize
@response
def bid_project(request, project_id):
    """
    竞标项目
    """
    params = json.loads(request.body)
    service = ProjectService()
    # 判断是否已经参与竞标
    has_been_bided = service.get_bid_project_info(request.user, project_id)

    # 已经参与了竞标，新的，更信息
    if has_been_bided is not None:
        is_updated, code = service.update_bid_info(project_id, request.user, params)
        if not is_updated:
            return {'code': code}
        else:
            return {'code': 200}
    during_biding = service.get_project_by_id(project_id=project_id)
    if during_biding.get('status', None) != '2':
        return {'code': 10115}
    service.bid_project(project_id, request.user, params)
    return {'code': 200}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=BidProjectListSerializer,
                     responses={'200': project_list_response})
@api_view(['POST'])
@authorize
@response
def bid_project_list(request):
    """
    项目竞标列表
    """
    if request.user.customer_type != '2':
        return {'code': 10117}
    params = json.loads(request.body)
    offset = params.get('offset', '0')
    limit = params.get('limit', '10')
    if isinstance(offset, str):
        offset = int(offset)
    if isinstance(limit, str):
        limit = int(limit)
    company_id = request.user.user_company.first().id
    count, data = ProjectService().get_bid_project_list(company_id=company_id,
                                                        query=params,
                                                        offset=offset, limit=limit)
    return {'code': 200, 'count': count, 'data': data}


@csrf_exempt
@swagger_auto_schema(methods=['get'],  responses={'200': bid_detail_response})
@api_view(['GET'])
@authorize
@response
def bid_detail(request, project_id):
    """
    竞标详情
    """
    data = ProjectService().get_multi_bid_info(request.user, project_id)
    return {'code': 200, 'data': data}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=ProjectListSerializer,
                     responses={'200': project_list_response}, )
@api_view(['POST'])
@authorize
@response
def project_list(request):
    """
    项目列表
    """
    params = json.loads(request.body)
    offset = params.get('offset', '0')
    limit = params.get('limit', '10')
    if isinstance(offset, str):
        offset = int(offset)
    if isinstance(limit, str):
        limit = int(limit)
    service = ProjectService()
    if request.user.customer_type == '1':
        proprietor_id = request.user.proprietor_user.first().id
        total_count, data = service.get_project_list(proprietor_id, params, offset, limit, is_owner=True)
        return {'code': 200, 'count': total_count, 'data': data}
    elif request.user.customer_type == '2':  # 中介项目列表
        total_count, data = service.get_project_list(query=params, offset=offset, limit=limit, is_owner=False)
        return {'code': 200, 'count': total_count, 'data': data}
    else:
        return {'code': 200}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=SendMessageSerializer,
                     responses={200: ''})
@api_view(['POST'])
@throttle_classes([IPThrottleForSendMessage, PhoneThrottleForSendMessage])
@response
def send_message(reqeust):
    """
    短信验证
    """
    body = reqeust.body
    if body is None:
        return {'code': 10103}
    params = json.loads(body)
    phone = params.get('phone')
    if phone is None:
        return {'code': 10103}
    is_send, code = SendMessage().send(['86'+phone])
    if is_send is True:
        UserService().insert_verify_code(phone, code)  # 保存验证码记录
        return {'code': 200}
    return {'code': 20021}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=ActiveSeriallizer,
                     responses={200: ''})
@api_view(['POST'])
@authorize
@response
def response_medium(request):
    """
    业主回复中介
    """

    if request.body is None:
        return {'code': 10103}
    data = json.loads(request.body)
    owner_response = data.get('owner_response', None)
    bid_id = data.get('bid_id', None)
    if bid_id is None or owner_response is None:
        return {'code': 10103}
    is_update, code = ProjectService().owner_response_medium(bid_id, owner_response)
    return {'code': code}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=BidPorjectListSerializer,
                     responses={'200': company_bid_list_response})
@api_view(['POST'])
@authorize
@response
def company_bid_projects(request):
    """
    中介的竞标列表
    """
    params = json.loads(request.body)
    offset = params.get('offset', '0')
    limit = params.get('limit', '10')
    if isinstance('offset', str):
        offset = int(offset)
    if isinstance('limit', str):
        limit = int(limit)
    total_count, data = ProjectService().get_medium_bid_project_list(request.user, params, offset, limit)
    return {'code': 200, 'count': total_count, 'data': data}


@csrf_exempt
@api_view(['GET'])
@response
def test_task(request, project_id):
    AuditService.finish_biding_project(project_id)
    return {'code': 200}
