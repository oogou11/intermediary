"""
业务code码
"""
from datetime import datetime
from functools import wraps
from rest_framework.response import Response
from api.views import UserService
import logging

logger = logging.getLogger('collect')


code_info = {
    # http 码
    200: 'success',
    500: '系统异常',
    # 业务相关code
    10100: '上传的文件不能为空!',
    10101: '上传文件格式有误!',
    10102: '资质审核不通过!',
    10103: '缺少必要参数!',
    10104: '文件不存在!',
    10105: '审核类型有误!',
    10106: '操作失败,未知错误,请联系管理员!',
    10107: '竞标信息最允许更改3次!',
    10108: '非业主身份,无权操作!',
    10109: '无权操作!',
    10110: '今日请求已达上线!',
    10111: '项目不存在!',
    10112: '该项目不可更改!',
    10113: '该中介机构未参与竞标',
    10114: '不可重复竞标!',
    10115: '非竞标期!',
    10116: '数据不存在!',
    10117: '非中介机构,无权操作!',
    # end

    # 用户相关code
    20001: '帐号或密码有误!',
    20010: '用户名不能为空!',
    20011: '密码不能为空!',
    20012: '两次输入的密码不一致!',
    20013: '邮箱不能为空!',
    20014: '手机不能为空!',
    20015: '用户类型非法!',
    20016: '用户类型有误!',
    20017: '用户名已经存在!',
    20018: '非驳回状态下，业主信息不允许修改!',
    20019: '信息不允许修改，请联系管理员!',
    20020: '验证码有误!',
    20021: '短信发送失败!',
    20022: '该服务类型不存在!',
    20023: '咨询次数到达上线!',
    20024: '回复次数到达上线!',
    20025: '非业务交互类型',
    20026: '业主未回复,不可重复竞标!',
    20027: '竞标信息不存在！',
    # end
}


def message(code):
    msg = code_info.get(code, 'success')
    return {'code': code, 'msg': msg}


def response(func):
    """
    API接口统一返回JSON格式
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = {'code': 200}
        _request = args[0]._request
        logging.info('请求开始:{}'.format(datetime.now()))
        logger.info(
            'time:{};\napi:{};\nheader:{};\nbody:{};\n'.format(datetime.now(),
                                                               _request.path,
                                                               _request.headers,
                                                               _request.body
                                                               ))
        try:
            result = func(*args, **kwargs)  # 方法执行的结果
            msg = message(result.get('code', 200))
            res = {**result, **msg}
        except Exception as ex:
            logger.error('请求出错：{}'.format(str(ex)))
            res.update({'code': 500, 'msg': '系统异常!'})
        finally:
            return Response(res)
    return wrapper


def authorize(func):
    """
    授权认证
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        _request = args[0]._request  # 记录请求日志
        token = _request.META.get("HTTP_AUTHORIZATION")  # 获取Token
        logging.info('请求开始:{}'.format(datetime.now()))
        logger.info(
            'time:{};\napi:{};\nheader:{};\nbody:{};\n'.format(datetime.now(),
                                                               _request.path,
                                                               _request.headers,
                                                               _request.body
                                                               ))
        # 如果是中介图片不需要授权
        if _request.path == '/api/download/' and _request.GET.get('role', None) == '2':
            return func(*args, **kwargs)
        # 判断token是否为空
        if token is None:
            return Response(status=401)
        # 判断token是否过期
        is_exists, user = UserService().get_user_by_token(token)
        if not is_exists:
            return Response(status=403)
        else:
            args[0].user = user
        return func(*args, **kwargs)
    return wrapper


def check_params(func):
    """
    请求参数校验
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


