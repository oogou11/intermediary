"""
model: Token、User
"""
import time
import datetime
from hashlib import md5
from django.conf import settings
from basedb.models import User, UserToken
from basedb.models import ProprietorProfile, IntermediaryProfile
from basedb.models import Project, BidProject, Interactive, ServeType, SectionType
from basedb.models import AuditLog, VerifyCode
from django.db import transaction
import logging
collect_logger = logging.getLogger('collect')
error_logger = logging.getLogger('error')


class UserService(object):
    """
    用户业务层
    """
    def get_user_by_username(self, username):
        """
        根据用户名获取用户
        :param username:
        :return:
        """
        data = User.objects.filter(username=username).first()
        return data

    def get_user_by_id_to_dict(self, user_id):
        """
        通过user id获取用户信息
        :param user_id:
        :return:
        """
        user = User.objects.filter(id=user_id).first()
        res = {
            'username': user.username,
            'customer_type': user.customer_type,
            'phone': user.phone,
            'email': user.email,
        }
        # 中介有评分
        if user.customer_type == '2':
            res.update({'rate': user.rate})
        return res

    def get_user_by_id(self, user_id):
        """
        获取用户
        :param user_id:
        :return:
        """
        user = User.objects.get(id=user_id)
        return user

    def get_user_by_username_and_password(self, username, password):
        """
        根据用户名和密码获取用户信息
        :param username: 用户名
        :param password: 密码
        :return:
        """
        data = User.objects.filter(username=username, password=md5(password.encode()).hexdigest()).first()
        return data

    def update_user_profile(self, user_id, data):
        """
        更新用户基本信息
        :param user_id: 用户ID
        :param data: 更新数据
        :return:
        """
        data = User.objects.filter(id=user_id).update(**data)
        return data

    def update_toke(self, user):
        """
        删除token
        :param user:
        :return:
        """
        hash_data = '{}-{}-{}-{}'.format(user.id, user.password, settings.SECRET_KEY, str(time.time()))
        res = md5(hash_data.encode()).hexdigest()
        expire_time = datetime.timedelta(days=1)
        user_token = UserToken.objects.get(user=user)
        user_token.token = res
        user_token.expiration_time = datetime.datetime.now() + expire_time
        user_token.save()
        return res

    def create_token(self, user):
        """
        生成token
        :return:
        """
        hash_data = '{}-{}-{}-{}'.format(user.id, user.password, settings.SECRET_KEY, str(time.time()))
        res = md5(hash_data.encode()).hexdigest()
        expire_time = datetime.timedelta(days=1)
        UserToken(user=user, token=res, expiration_time=datetime.datetime.now()+expire_time).save()
        return res

    def create_user(self, username, password, phone, email, customer_type="1"):
        """
        用户注册
        :param username: 用户名
        :param password: 密码
        :param customer_type: 默认是业主
        :return:
        """
        md5_pwd = md5(password.encode()).hexdigest()  # 密码加密
        User(username=username,
             password=md5_pwd,
             customer_type=customer_type,
             phone=phone,
             email=email).save()

    def insert_verify_code(self, phone, code):
        """
        保存验证码
        :param phone:
        :param code:
        :return:
        """
        vf = VerifyCode()
        vf.phone = phone
        expire_time = datetime.timedelta(minutes=1)  # 1分钟后过期
        vf.expire_time = datetime.datetime.now() + expire_time
        vf.verify_code = code
        vf.save()
        return vf.id

    def reset_password(self, username, phone, password):
        """
        重置密码
        :param username:
        :param phone:
        :return:
        """
        data = User.objects.filter(username=username, phone=phone)
        if data.first() is None:
            return False
        md5_pwd = md5(password.encode()).hexdigest()  # 密码加密
        data.update(**{'password': md5_pwd})
        return True

    def check_phone_code(self, phone, code):
        """
        检验验证码
        :param phone:
        :param code:
        :return:
        """
        data = VerifyCode.objects.filter(phone=phone, verify_code=code).first()
        if data is None:
            return False
        if datetime.datetime.now() > data.expire_time:
            return False
        return True

    def owner_detail(self, user_id):
        """
        用户详情
        :param user_id:
        :return:
        """
        res = dict()
        data = ProprietorProfile.objects.filter(user__id=user_id).first()
        if data is None:
            return res

        res.update({'business_id': data.id,
                    'organization_code': data.organization_code,
                    'organization_name': data.organization_name,
                    'corporation': data.corporation,
                    'id_card_number': data.id_card_number,
                    'organization_picture': data.organization_picture,
                    'status': data.status,
                    'status_name': list(filter(lambda x: x[0] == data.status,
                                               ProprietorProfile.STATUS_TYPE))[0][1],
                    'create_time': data.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    })
        return res

    def company_detail(self, user_id):
        """
        中介详情
        :param user_id:
        :return:
        """
        data = IntermediaryProfile.objects.get(user__id=user_id)
        res = self._get_company_detail_dict(data)
        return res

    def _get_company_detail_dict(self, data):
        res = dict()
        qualification_list = list()
        if data.qualification_info:
            for item in data.qualification_info:
                qualification_list.append({
                    'name': item.get('name', ''),
                    'url':  item.get('url', '')
                })
        if data.enterprise_type is not None:
            enterprise_type_name = list(filter(lambda x: x[0] == data.enterprise_type,
                                               IntermediaryProfile.ENTERPRISE_TYPE))[0][1]
        else:
            enterprise_type_name = ''
        res.update({
            'intermediary_id': data.id,
            'organization_code': data.organization_code,
            'organization_name': data.organization_name,
            'corporation': data.corporation,
            'service_type': data.service_type.id if data.service_type else '',
            'service_type_name': data.service_type.server_name if data.service_type else '',
            'enterprise_type': data.enterprise_type,
            'enterprise_type_name': enterprise_type_name,
            'section_id': data.service_type.section_id.id if data.service_type else '',
            'section_name': data.service_type.section_id.section_name if data.service_type else '',
            'service_content': data.service_content,
            'address': data.address,
            'is_union': data.is_union,
            'id_card_front_url':  data.id_card_front_url,
            'id_card_back_url': data.id_card_back_url,
            'remark': data.remark,
            'contract_person': data.contract_person,
            'co_id_card_front_url':   data.co_id_card_front_url,
            'co_id_card_back_url':   data.co_id_card_back_url,
            'authorize_url':  data.authorize_url if data.authorize_url else '',
            'qualification_info': data.qualification_info,
            'qualification_list': qualification_list,
            'status': data.status,
            'status_name': list(filter(lambda x: x[0] == data.status, data.Status))[0][1]
        })

        return res

    def update_owner_info(self, user, data):
        """
        更新业主信息
        :param data:
        :return:
        """
        data.update({'user': user})
        owner = ProprietorProfile.objects.filter(user=user)
        # 为空新增
        if owner.count() == 0:
            new_owern = ProprietorProfile()
            for name, value in data.items():
                setattr(new_owern, name, value)
            new_owern.save()
            return True, new_owern.id
        # 非驳回状态不允许修改
        first_data = owner.first()
        if first_data.status not in ('0' '3'):
            return False, None
        owner.update(**data)
        return True, first_data.id

    def get_company_info(self, company_id):
        """
        获取中介详情
        :param company_id:
        :return:
        """
        data = IntermediaryProfile.objects.get(id=company_id)
        return data

    def get_company_list(self, service_type=None, company_name=None,
                         rate_start=None, rate_end=None,
                         offset=0, limit=10):
        """
        获取中介列表
        :param service_type:
        :return:
        """
        params = {'status': '2'}
        if service_type is not None:
            params.update({'service_type': service_type})
        if company_name is not None:
            params.update({'organization_name__contains': company_name})
        if rate_start is not None:
            params.update({'user__rate__gte': rate_start})
        if rate_end is not None:
            params.update({'user__rate__lte': rate_end})
        all_data = IntermediaryProfile.objects.filter(**params)
        total_count = all_data.count()
        data = all_data[offset: limit]

        res = list()
        for item in data:
            inner_item = self._get_company_detail_dict(item)
            res.append(inner_item)
        return total_count, res

    def check_service_type(self, service_type):
        """
        检验中介的服务类型是否合法
        :param service_type:
        :return:
        """
        data = ServeType.objects.filter(id=service_type).first()
        if data is None:
            return False, None
        return True, data

    def update_company_info(self, user, data):
        """
        更新中介新
        :param user: 用户
        :param data: 更新数据
        :return:
        """
        data.update({'user': user})
        company = IntermediaryProfile.objects.filter(user=user)
        # 为空新增
        if company.count() == 0:
            new_company = IntermediaryProfile()
            for name, value in data.items():
                setattr(new_company, name, value)
            new_company.save()
            return True, new_company.id
        first_company = company.first()
        if first_company.status not in ('0', '3'):
            return False, None
        company.update(**data)
        return True, first_company.id

    def get_user_by_token(self, token):
        """
        判断token是否已经过期
        :param token:
        :return:
        """
        data = UserToken.objects.filter(token=token).first()
        if data is None:
            return False, None
        if datetime.datetime.now() > data.expiration_time:
            return False, None
        return True, data.user



class ServiceTypeService(object):
    """
    服务类型
    """

    def add_service_type_list(self, data):
        """
        新增服务器类型
        :param data:
        :return:
        """
        ServeType(**data).save()
        return True

    def get_service_type_list(self, section_id=None, section_name=None, server_name=None):
        """
        获取服务类型列表
        :return:
        """
        query = dict()
        if server_name is not None:
            query.update({'server_name__contains': server_name})
        if section_id is not None:
            query.update({'section_id': section_id})
        if section_name is not None:
            query.update({'section_id__section_name__contains': section_name})
        data = ServeType.objects.filter(**query)
        res = list()
        for item in data:
            res.append({
                'section_id': section_id.id if section_id else '',
                'section_name': section_id.section_name if section_id else '',
                'id': item.id,
                'server_name': item.server_name
            })
        return res

    def get_section_list(self, section_id=None, section_name=None):
        query = dict()
        if section_id is not None:
            query.update({'id': section_id})
        if section_name is not None:
            query.update({'section_name__contains': section_name})

        data = SectionType.objects.filter(**query)
        res = list()
        for item in data:
            res.append({
                'id': item.id,
                'section_name': item.section_name
            })
        return res




class ProjectService(object):
    """
    项目相关
    """
    def get_project_by_id(self, project_id, is_website=False, is_owner=True):
        """
        获取项目详情
        :param project_id:
        :return:
        """
        project = Project.objects.get(id=project_id)
        res = self._get_project_detail_dict(project, is_website, is_owner)
        return res

    def _get_project_detail_dict(self, project, is_website=False, is_owner=True):
        """
        项目详情字段
        :param project:
        :return:
        """
        bid_person = project.bid_projects.filter(is_active=True)
        bid_company = list()
        if not is_website and is_owner:
            for item in bid_person:
                bid_company.append({
                    'bid_id': item.id,
                    'intermediary_id': item.bid_company.id if item.bid_company else '',
                    'intermediary_name': item.bid_company.organization_name if item.bid_company else '',  # 中介公司
                    'bid_describe': item.describe,  # 竞标描述
                    'bid_money': item.bid_money,  # 竞标金额
                    'status': item.status,
                    'status_name': list(filter(lambda x: x[0] == item.status, BidProject.STATUS))[0][1]
                })
        res = {
            'id': project.id,
            'project_name': project.project_name,
            'contract_person': project.contract_person,
            'contract_phone': project.contract_phone,
            'project_scale': project.project_scale,  # 项目规模
            'service_low_count': project.service_low_count,  #
            'service_high_count': project.service_high_count,
            'choice_type': project.choice_type,
            'choice_type_name': list(filter(lambda x: x[0] == project.choice_type, Project.CHOICE_TYPE))[0][1],
            'content': project.content,  # 项目内容
            'qualification': project.qualification,
            'qualification_name': list(filter(lambda x: x[0] == project.qualification, Project.User_Qualifications))[0][
                1],
            'begin_time': project.begin_time.strftime('%Y-%m-%d %H:%M:%S'),
            'finish_time': project.finish_time.strftime('%Y-%m-%d %H:%M:%S'),
            'project_limit': project.project_limit,
            'bid_company': bid_company,
            'bid_company_count': bid_person.count(),
            'status': project.status,
            'status_name': list(filter(lambda x: x[0] == project.status, Project.STATUS_TYPE))[0][1],
            'remark': project.file_url,
            'file_url': project.file_url,
            'contract': project.contract,
            'sys_info': project.sys_info,
            'server_type': project.server_type.id if project.server_type else '',
            'server_type_picture_url': project.server_type.picture_url if project.server_type else '',
            'server_type_name': project.server_type.server_name if project.server_type else '',
        }
        return res

    def get_project_list(self, proprietor_id=None, query={}, offset=0, limit=10, is_website=False, is_owner=True):
        """
        获取项目列表
        :param offset:
        :param limit:
        :return:
        """
        res = list()
        total_count, data = self._get_project_data(query, proprietor_id, offset, limit)
        for item in data:
            inner_item = self._get_project_detail_dict(item, is_website, is_owner)
            res.append(inner_item)
        return total_count, res

    def _get_project_data(self, query, proprietor_id=None, offset=0, limit=10):
        """
        获取查询结构
        :param params:
        :return:
        """
        params = dict()
        if query.get('status', None) is not None:
            params.update({'status': query.get('status')})
        if query.get('project_name', None) is not None:
            params.update({'project_name__contains': query.get('project_name')})
        if query.get('choice_type', None) is not None:
            params.update({'choice_type': query.get('choice_type')})
        if query.get('proprietor_name', None) is not None:
            params.update({'proprietor__organization_name__contains': query.get('proprietor_name')})
        if query.get('server_type', None) is not None:
            params.update({'server_type__in': query.get('server_type', [])})
        if query.get('section_name', None) is not None:
            params.update({'server_type__section_id__section_name': query.get('section_name', '')})
        if query.get('choice_type', None) is not None:
            params.update({'choice_type':  query.get('choice_type')})
        if query.get('query_contract', False):
            # 查询合同
            params.update({'contract__isnull': False})
        if proprietor_id is not None:
            params.update({'proprietor__id': proprietor_id})
        if query.get('has_bid_project', None) == 1:
            # 参与竞标的项目
            params.update({'bid_project_intermediary__bid_company': query.get('intermediary_id')})

        all_data = Project.objects.filter(**params).order_by('begin_time')
        total_count = all_data.count()
        data = all_data[offset:limit]
        return total_count, data

    def create_project(self, user, data):
        """
        创建项目
        :param user: 业主
        :param data: 参数
        :return:
        """
        begin_time = data.get('begin_time')
        finish_time = data.get('finish_time')
        data.update({'begin_time': datetime.datetime.strptime(begin_time, '%Y-%m-%d %H:%M:%S'),
                     'finish_time': datetime.datetime.strptime(finish_time, '%Y-%m-%d %H:%M:%S'),
                     'create_user': user,
                     'proprietor': user.proprietor_user.first(),
                     })
        pro = Project()
        for name, value in data.items():
            setattr(pro, name, value)
        pro.save()
        return pro.id

    def update_project(self, user, project_id, data):
        """
        编辑项目资料
        :param project_id: 项目ID
        :param data: 更新值
        :return:
        """
        pro = Project.objects.filter(id=project_id)
        pro_first = pro.first()
        if pro_first is None:
            return False, 10111
        if user.id != pro_first.create_user.id:
            return False, 10108
        if pro_first.status != '0':
            return False, 10112
        pro.update(**data)
        return True, 200

    def score_company(self, project_id, data):
        """
        评分
        :param project_id:
        :return:
        """
        score_level_one = data.get('score_level_one', 0)
        score_level_two = data.get('score_level_two', 0)
        score_level_three = data.get('score_level_three', 0)
        score_level_four = data.get('score_level_four', 0)
        score_level_five = data.get('score_level_five', 0)
        # 平均分
        avarage_score = (score_level_one + score_level_two + score_level_three
                         + score_level_four + score_level_five) / 5
        data.update({'average_score': avarage_score})

        project_info = Project.objects.filter(id=project_id)

        # 获取中标的中介
        win_bid_project_info = project_info.first().bid_projects.filter(status=1).first()
        # 中标过的所有项目
        bid_all_projects = BidProject.objects.filter(bid_company=win_bid_project_info.bid_company.id)
        with transaction.atomic():
            # 更新用户总评分
            new_score = 0
            for c in bid_all_projects:
                new_score += c.project.average_score
            # 总评分重新计算
            new_score = (new_score+avarage_score) / bid_all_projects.count()

            # 更新User的rate总评分
            user_id = bid_all_projects.first().bid_user.id
            # 最后评分
            if win_bid_project_info.bid_company.super_rate is not None:  # 兼容旧数据
                new_score = (new_score + win_bid_project_info.bid_company.super_rate) / 2

            User.objects.filter(id=user_id).update(**{'rate': int(new_score),
                                                      'update_time': datetime.datetime.now()})

            project_info.update(**data)
        return True


    def bid_project(self, project_id, user, data):
        """
        投标
        :param project_id: 项目ID
        :param user: 竞标人
        :param data: 竞标信息
        :return:
        """
        project = Project.objects.get(id=project_id)
        data.update({'bid_user': user,
                     'project': project,
                     'bid_company': user.user_company.first()})
        BidProject(**data).save()
        return True

    def get_bid_info_by_id(self, bid_id):
        """
        获取竞标详情
        :param bid_id: 竞标ID
        :return:
        """
        data = BidProject.objects.get(id=bid_id)
        res = {
            'id': bid_id,
            'project_id': data.project.id,
            'project_name': data.project.project_name,
            'bid_money': data.bid_money,
            'files_info': data.files_info,
            'describe': data.describe,
            'create_time': data.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': data.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': data.status,
            'status_name': list(filter(lambda x: x[0] == data.status, BidProject.STATUS))[0][1],
            'score_level_one': data.project.score_level_one,
            'score_level_two': data.project.score_level_two,
            'score_level_three': data.project.score_level_three,
            'score_level_four': data.project.score_level_four,
            'score_level_five': data.project.score_level_five,
            'owner_response': data.owner_response,
        }
        return res

    def get_multi_bid_info(self, user, project_id):
        """
        获取项目的竞标信息
        :param user:
        :param project_id:
        :return:
        """
        data = BidProject.objects.filter(bid_user=user.id, project=project_id).order_by('-create_time')
        res = list()
        for item in data:
            res.append({
                'id': item.id,
                'project_id': item.project.id,
                'project_name': item.project.project_name,
                'bid_money': item.bid_money,
                'files_info': item.files_info,
                'describe': item.describe,
                'create_time': item.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': item.update_time.strftime('%Y-%m-%d %H:%M:%S') if item.update_time is not None else '',
                'status': item.status,
                'status_name': list(filter(lambda x: x[0] == item.status, BidProject.STATUS))[0][1],
                'owner_response': item.owner_response,
            })
        return res

    def get_bid_project_list(self, company_id, query=dict, offset=0, limit=10):
        """
        获取竞标的项目列表
        :param user:
        :return:
        """
        params = {'bid_company': company_id}
        if query.get('project_name', None) is not None:
            params.update({'project__project_name__contains': query.get('project_name')})
        if query.get('status', None) is not None:
            params.update({'status': query.get('status')})
        all_data = BidProject.objects.filter(**params)
        total_count = all_data.count()
        data = all_data[offset:limit]
        res = list()
        for item in data:
            inner_item = self._get_project_detail_dict(item.project, is_owner=False)
            res.append(inner_item)
        return total_count, res

    def get_bid_project_info(self, user=None, project_id=None, status=None):
        """
        获取投标信息
        :param user: 投标人
        :param project_id: 项目ID
        :param status: 项目状态
        :return:
        """
        params = dict()
        if user is not None:
            params.update({'bid_user': user.id})
        if project_id is not None:
            params.update({'project': project_id})
        if status is not None:
            params.update({'project__status': status})
        data = BidProject.objects.filter(**params).first()
        return data

    def select_bid_company(self, project_id, intermediary_id):
        """
        选标
        :param project_id: 项目ID
        :param intermediary_id: 中介机构ID
        :return:
        """
        data = BidProject.objects.filter(project=project_id, bid_company=intermediary_id)
        if data.first() is None:
            return False, 10113
        data.update(**{'status': '1'})
        pro = Project.objects.get(id=project_id)
        pro.status = '4'
        pro.save()
        return True, 200

    def update_bid_info(self, project_id, medium_user, data):
        """
        更新竞标信息
        :param medium_user: 中介
        :param data: 竞标信息
        :return:
        """
        # 获取之前的竞标信息，并批量制成无效
        bid_info = BidProject.objects.filter(bid_user=medium_user.id,
                                             project_id=project_id,
                                             is_active=True)
        # 判断是否已经有业主回复
        first_bid_info = bid_info.first()
        # 业主未回复，不可重复参与竞标
        if len(first_bid_info.owner_response.keys()) == 0:
            return False, 20026
        # 添加事物
        with transaction.atomic():
            try:
                bid_info.update(**{'is_active': False,
                                   'update_time': datetime.datetime.now()})  # 更改旧的竞标未无效
                self.bid_project(project_id, medium_user, data)  # 添加新的竞标信息
                return True, 200
            except Exception as ex:
                error_logger.error('time:{}，project_id:{},function:{},msg:{}'.
                                   format(datetime.datetime.now(),
                                          project_id,
                                          'update_bid_info',
                                          ex))
                return False, 500

    def owner_response_medium(self, bid_id, data):
        """
        业主回复竞标信息
        :param bid_id: 竞标ID
        :return:
        """
        try:
            bid_info = BidProject.objects.get(id=bid_id)
            bid_info.owner_response = data
            bid_info.update_time = datetime.datetime.now()
            bid_info.save()
            return True, 200
        except Exception as ex:
            return False, 20027

    def get_medium_bid_project_list(self, user, query=dict, offset=0, limit=10):
        """
        获取中介的竞标列表
        :param user:
        :return:
        """
        params = {'bid_user': user.id}
        if query.get('project_name', None) is not None:
            params.update({'project__project_name__contains': query.get('project_name')})
        if query.get('proprietor_name', None) is not None:
            params.update({'project__proprietor__organization_name__contains':
                           query.get('proprietor_name')})
        all_data = BidProject.objects.filter(**params).order_by('-create_time')
        # 相同项目 只获取最新的一条
        res = list()
        project_id = None
        total_count = all_data.count()
        data = all_data[offset: limit]
        for item in data:
            if item.project.id == project_id:
                continue
            res.append({
                'id': item.id,
                'project_id': item.project.id,
                'project_name': item.project.project_name,
                'proprietor': item.project.proprietor.organization_name,  # 业主
                'create_time': item.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': item.status,
                'status_name': list(filter(lambda x: x[0] == item.status, BidProject.STATUS))[0][1]
            })
            project_id = item.project.id
        return total_count, res




class AuditService(object):
    """
    管理员审核信息
    """

    def update_user_status(self, user_id):
        """
        增加业主审核信息
        :param owner_id: 业主ID
        :return:
        """
        user = User.objects.get(id=user_id)
        user.status = '3'  # 审核中
        user.save()
        return True

    def add_company_audit(self, company_id):
        """
        增加中介审核信息
        :param company_id: 中介ID
        :return:
        """
        AuditLog(audit_type='1',
                 business_id=company_id).save()

    def add_project_audit(self, project_id):
        """
        增加项目审核信息
        :param project_id: 项目ID
        :return:
        """
        AuditLog(audit_type='3',
                 business_id=project_id).save()

    def audit_owner(self, user, owner_id, audit_id, content, status):
        """
        审核业主资料
        :param user: 审核人
        :param owner_id: 业务ID
        :param content: 审核内容
        :param status: 审核状态
        :return:
        """
        with transaction.atomic():
            is_updated = True
            try:
                owner = ProprietorProfile.objects.get(id=owner_id)
                owner.status = status
                owner.save()
                audit = AuditLog.objects.get(id=audit_id)
                audit.content = content
                audit.status = status
                audit.user = user
                audit.save()
            except Exception as ex:
                error_logger.error('time:{},function:{},msg:{}'.format(datetime.datetime.now(),
                                                                       'audit_owner',
                                                                       ex))
                is_updated = False, None
            finally:
                return is_updated, owner

    def audit_company(self, user, company_id, audit_id, content, status):
        """
        审核中介资料
        :param user: 审核人
        :param company_id: 中介ID
        :param content: 审核内容
        :param status: 审核状态
        :return:
        """
        with transaction.atomic():
            is_updated = True
            try:
                company = IntermediaryProfile.objects.get(id=company_id)
                company.status = status
                company.save()
                audit = AuditLog.objects.get(id=audit_id)
                audit.content = content
                audit.status = status
                audit.user = user
                audit.save()
            except Exception as ex:
                error_logger.error('time:{},function:{},msg:{}'.format(datetime.datetime.now(),
                                                                       'audit_company',
                                                                       ex))
                is_updated = False, None
            finally:
                return is_updated, company

    def audit_project(self, user, project_id, audit_id, content, status):
        """
        审核项目
        :param user: 审核人
        :param project_id: 项目ID
        :param content: 审核内容
        :param status: 审核状态
        :return:
        """
        with transaction.atomic():
            is_updated = True
            try:
                pro = Project.objects.get(id=project_id)
                pro.status = status
                pro.save()
                audit = AuditLog.objects.get(id=audit_id)
                audit.content = content
                audit.status = status
                audit.user = user
                audit.save()
            except Exception as ex:
                error_logger.error('time:{},function:{},msg:{}'.format(datetime.datetime.now(),
                                                                       'audit_project',
                                                                       ex))
                is_updated = False, None
            finally:
                return is_updated, pro

    @classmethod
    def finish_biding_project(cls, project_id):
        """
        竞标项目结束，选择竞标人员
        :param project_id: 项目ID
        :return:
        """
        project = Project.object.get(id=project_id)
        if project.choice_type == '0':  # 择优选取
            is_selected = cls()._select_the_best(project)
        elif project.choice_type == '1':  # 竞价选取
            is_selected = cls()._select_price_lowest(project)
        elif project.choice_type == '2':  # 平均价选取
            is_selected = cls()._select_average_price(project)
        else:
            is_selected = False
        if not is_selected:
            project.status = '3'  # 只有该状态--选表中--业主才会干预选标
            project.sys_info = '系统无法自动选标，请人工选标!'
            project.save()

    @classmethod
    def abolish_project(cls, project_id):
        """
        是否作废
        :param project_id:
        :return:
        """
        pro = Project.object.get(id=project_id)
        if pro.status not in('4', '5'):  # 选标、结束
            pro.status = '6'  # 作废
            pro.project_message = '该项目再规定时间内未完成选标，因此系统自动判断未作废'
            pro.save()

    def _select_the_best(self, project):
        """
        择优选取，选择被评分最高的
        :param project:
        :return:
        """
        with transaction.atomic():
            try:
                bid_companies = project.bid_projects.order_by('-bid_user__rate')
                first_rate = bid_companies.frist().bid_user__rate

                # 相同评分的 人工选标
                for i in range(1, bid_companies.count() - 1):
                    if bid_companies[i].bid_user__rate == first_rate:
                        return False
                bid_company = bid_companies.first()
                if bid_company is not None:
                    bid_company.status = '2'  # 中标
                    bid_company.save()
                    project.status = '4'  # 已选表
                    project.save()
                    return True
            except Exception as ex:
                error_logger.error('time:{}，project_id:{},function:{},msg:{}'.
                                   format(datetime.datetime.now(),
                                          project.id,
                                          '_select_the_best',
                                          ex))
                return False

    def _select_price_lowest(self, project):
        """
        选择报价最低的
        :param project:
        :return:
        """
        with transaction.atomic():
            try:
                bid_companies = project.bid_projects.order_by('-bid_money')
                bid_company = bid_companies.first()

                # 相同最低价格，人工选标
                for i in range(1, bid_companies.count() - 1):
                    if bid_companies[i].bid_money == bid_company.bid_money:
                        return False
                if bid_company is not None:
                    bid_company.status = '2'  # 中标
                    bid_company.save()
                    project.status = '4'  # 已选表
                    project.save()
                    return True
            except Exception as ex:
                error_logger.error('time:{}，project_id:{},function:{},msg:{}'.
                                   format(datetime.datetime.now(),
                                          project.id,
                                          '_select_price_lowest',
                                          ex))
                return False

    def _select_average_price(self, project):
        """
        选择离平均价最接近的
        :param project:
        :return:
        """
        bid_companies = project.bid_projects.all()
        total_money = 0
        n = 0
        for item in bid_companies:
            total_money += item.bid_money
            n += 1
        average_money = total_money / n
        index = 0
        for i in range(1, len(bid_companies) - 1):
            if abs(average_money) > abs(bid_companies[i].bid_money):
                average_money = bid_companies[i].bid_money
                index = i
        bid_company = bid_companies[index]

        current_money = bid_company.bid_money

        total_count = 0
        for com in bid_companies:
            if com.bid_company == current_money:
                total_count += 1

        # 有多个相同价格的
        if total_count > 1:
            return False

        with transaction.atomic():
            try:
                bid_company.status = '2'  # 中标
                bid_company.save()
                project.status = '4'  # 已选表
                project.save()
                return True
            except Exception as ex:
                error_logger.error('time:{}，project_id:{},function:{},msg:{}'.
                                   format(datetime.datetime.now(),
                                          project.id,
                                          '_select_price_lowest',
                                          ex))
                return False


class AggregateDataService(object):
    """
    聚合统计
    """
    def get_project_count(self, params=None):
        """
        项目聚合
        :param params:
        :return:
        """
        count = Project.objects.count()
        return {'project_count': count}


    def get_owern_count(self, params=None):
        """
        业主聚合
        :param params:
        :return:
        """
        count = ProprietorProfile.objects.count()
        return {'owner_count': count}

    def get_intermediary_count(self, params=None):
        """
        中介总数
        :param params:
        :return:
        """
        count = IntermediaryProfile.objects.count()
        return {'intermediary_count': count}

