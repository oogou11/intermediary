import json
import gevent
from api.service import *
from api.serializer import *
from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.csrf import csrf_exempt
from utils.code import response
from rest_framework.decorators import api_view


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=ProjectListSerializer,
                     responses={200: ''})
@api_view(['POST'])
@response
def project_list(request):
    """
    项目列表
    请求参数:
    {"project_name": "项目名称",
    "proprietor_name": "项目业主",
    "choice_type": "选取方式",
    "server_type": ["服务类型1", "服务类型2"]
    "section_name": "对应的部门"
    "query_type": 1, 1-普通查询，2-中标查询 3-合同查询
    "offset": 0, "limit": 10}
    返回结果:
    {
        "code": 200,
        "msg": "success",
        "count": "总条数",
        "data": [
            {

            }
        ]
    }
    """
    params = json.loads(request.body)
    offset = params.get('offset', '0')
    limit = params.get('limit', '10')
    if isinstance(offset, str):
        offset = int(offset)
    if isinstance(limit, str):
        limit = int(limit)
    query_type = params.get('query_type', None)
    if query_type is not None:
        # 转换成整型
        if isinstance(query_type, str):
            query_type = int(query_type)
        # 采购公告
        if query_type == 1:  # 竞标中
            params.update({'status': '2'})
        if query_type == 2:  # 中选机构列表
            params.update({'status': '4'})
        if query_type == 3:  # 有合同的项目列表
            params.update({'query_contract': True})
    service = ProjectService()
    total_count, data = service.get_project_list(query=params, offset=offset, limit=limit, is_website=True)
    return {'code': 200, 'count': total_count, 'data': data}


@csrf_exempt
@swagger_auto_schema(methods=['post'], request_body=CompanyListSerializer,
                     responses={200: ''})
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
        rate_start = params.get('rate_start', '0')
        rate_end = params.get('rate_end', '0')
    if isinstance(offset, str):
        offset = int(offset)
    if isinstance(limit, str):
        limit = int(limit)
    total_count, data = UserService().get_company_list(service_type=service_type,
                                                       company_name=company_name,
                                                       rate_start=rate_start,
                                                       rate_end=rate_end,
                                                       offset=offset,
                                                       limit=limit)
    return {'code': 200, 'count': total_count, 'data': data}


@csrf_exempt
@swagger_auto_schema(methods=['get'], manual_parameters=[],
                     responses={200: ''})
@api_view(['GET'])
@response
def service_type(reqeust):
    """
    类型，不需要登录
    请求信息:
    返回结果:
    {
        "code": 200,
        "msg": "success",
        "data": [ {"id": 121, "server_name": "管理"} ] ]
    }
    """
    section_id = reqeust.GET.get('section_id', None)
    section_name = reqeust.GET.get('section_name', None)
    server_name = reqeust.GET.get('server_name', None)
    data = ServiceTypeService().get_service_type_list(section_id, section_name, server_name)
    return {'code': 200, 'data': data}


@csrf_exempt
@swagger_auto_schema(methods=['get'], manual_parameters=[],
                     responses={200: ''})
@api_view(['GET'])
@response
def section_type(reqeust):
    """
    类型，不需要登录
    请求信息:
    返回结果:
    {
        "code": 200,
        "msg": "success",
        "data":  [ {"id": 121, "section_name": "管理"} ]
    }
    """
    section_id = reqeust.GET.get('section_id', None)
    section_name = reqeust.GET.get('section_name', None)
    data = ServiceTypeService().get_section_list(section_id, section_name)
    return {'code': 200, 'data': data}


@csrf_exempt
@api_view(['GET'])
@response
def project_detail(request, project_id):
    """
    获取项目详情
    请求参数: project_id: 项目ID
    返回结果
    {
        "code": 200,
        "msg": "success",
        "total_bid_count": "",
        "data": {
            'id': "项目ID",
            'project_name': "项目名称",
            'content': "项目内容",
            'project_scale': "项目规模",
            'qualification': "资质等级"],
            'begin_time': "项目开始时间",
            'finish_time': "项目结束时间",
            'project_limit': "项目期限",
            'status': "项目状态code",
            'status_name': "状态名称",
            'bid_company': [
                'intermediary_id':  "中介公司ID",
                'intermediary_name': "中介公司名称",
                'bid_describe': "竞标描述",
                'bid_money': "竞标金额",
                'status':  "竞标状态code",
                'status_name': "竞标状态名称"
            ],
        }

    }
    """
    if project_id is None:
        return {'code': 10103}
    data = ProjectService().get_project_by_id(project_id, is_owner=False)
    return {'code': 200, 'data': data}


@csrf_exempt
@api_view(['GET'])
@response
def project_detail(request, project_id):
    """
    项目详情
    请求参数:
    """
    data = ProjectService().get_project_by_id(project_id, True, False)
    return {'code': 200, 'data': data}


@csrf_exempt
@api_view(['GET'])
@response
def get_aggregate_data(request):
    """
    聚合统计: 中介、业主、项目总量
    """
    service = AggregateDataService()
    task_reuslt = gevent.joinall([
        gevent.spawn(service.get_project_count),   # 项目总量
        gevent.spawn(service.get_owern_count),   # 业主总量
        gevent.spawn(service.get_intermediary_count)  # 中介总量
    ])
    data = dict()
    for item in task_reuslt:
        data = {**data, **item.value}
    return {'code': 200, 'data': data}


