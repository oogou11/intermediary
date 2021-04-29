from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20190711 import sms_client, models
from rest_framework.throttling import BaseThrottle
from rest_framework import exceptions
from django.conf import settings
import random
import datetime
from basedb.models import VerifyCode, MessageLog
import logging
import json

logger = logging.getLogger('message')


class SendMessage(object):
    """
    发送短信
    """
    def __init__(self):
        self.template = '测试短信'
        self.content = ''
        self.template_id = "932560"
        self.cred = credential.Credential(settings.MESSAGE_SECRETID, settings.MESSAGE_SECRETKEY)

    def _get_template(self, params):
        """
        配置模版
        :param params:
        :return:
        """
        try:
            # 申请短信模版
            client = sms_client.SmsClient(self.cred, "ap-guangzhou")
            req = models.AddSmsTemplateRequest()
            req.TemplateName = self.template
            req.TemplateContent = self.content
            resp = client.AddSmsTemplate(req)
            ten_data = resp.to_json_string(indent=2)

            # 日志
            logger.info('time:{}, tempalate api data:{}'.format(datetime.datetime.now(), ten_data))
        except TencentCloudSDKException as err:
            # 错误日志
            logger.error('time:{},msg template error: {}'.format(datetime.datetime.now(), err))

    def _get_verify_code(self):
        """
        随机生成6位-只能是数字
        # 48--57 ： 0-9
        # 65--90 ： A-Z
        # 97--122： a-z
        :return:
        """
        index = 6
        count = 0
        code = ""
        while index > count:
            num = random.randrange(48, 57)
            if num <= 57:  # 符合条件
                code += chr(num)
                count += 1
        return code

    def send(self, phone, template_id=None, params=None):
        """
        发送短信
        :param phone: 电话号码
        :param template_id: 短信模版ID
        :param params: 短信模版参数：["", ""]数组类型
        :return:
        """
        # 默认是短信注册验证模版
        if template_id is None:
            template_id = self.template_id
        # 短息模版参数
        if params is None:
            code = self._get_verify_code()
            params = [code, "1"]
        else:
            code = ''
        try:
            client = sms_client.SmsClient(self.cred, "ap-guangzhou")
            req = models.SendSmsRequest()
            req.SmsSdkAppid = settings.MESSAGE_APP_ID
            req.Sign = settings.MESSAGE_SIGN
            req.TemplateID = template_id  # 模版ID
            req.TemplateParamSet = params  # 模版参数
            req.PhoneNumberSet = ["+86{}".format(phone)]

            resp = client.SendSms(req)
            ten_res = resp.to_json_string(indent=2)
            json_res = json.loads(ten_res)
            send_status = json_res.get('SendStatusSet')

            logger.info('time:{}, send message:{}'.format(datetime.datetime.now(), json_res))

            # 存储数据
            if send_status[0].get('Code') == 'Ok':
                return True, code
        except TencentCloudSDKException as err:
            logger.error('time:{}, send message error:{}'.format(datetime.datetime.now(), err))
            return False, None


class IPThrottleForSendMessage(BaseThrottle):
    """
    IP限制: 通过设置setting中的 MESSAGE_IP_LIMIT_COUNT 参数进行次数的变更
    """
    def wait(self):
        """
        禁止1天
        :return:
        """
        return 24*60*60

    def allow_request(self, request, view):
        """
        是否运行请求
        :param request:
        :param view:
        :return:
        """
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            ip = request.META.get("REMOTE_ADDR")

        request_info = MessageLog.objects.filter(ip=ip)
        first_time = request_info.first()  # 获取第一条记录

        # 同一天的访问
        if first_time is not None and \
                first_time.update_time.date() == datetime.datetime.today().date():
            # 不是第一次访问
            new_count = first_time.count+1
            if first_time.count >= settings.MESSAGE_IP_LIMIT_COUNT:
                # 超过10次禁止访问
                request_info.update(**{'limit_count': new_count, 'update_time': datetime.datetime.now()})
                return self.throttle_failure()
            else:
                # 没超过5次可以访问
                request_info.update(**{'count': new_count, 'update_time': datetime.datetime.now()})
        else:
            # 第一次访问
            MessageLog(ip=ip).save()
        return True

    def throttle_failure(self):
        """
        禁止访问
        """
        class NewThrottled(exceptions.APIException):

            def __init__(self, detail=None, code=None):
                super().__init__(detail, code)

        raise NewThrottled(detail={'code': 10110, 'msg': '今日访问已达上线, 一天后才可以访问!'})


class PhoneThrottleForSendMessage(BaseThrottle):
    """
    手机号限制: 通过设置setting中的 MESSAGE_PHONE_LIMIT_COUNT 参数进行次数的变更
    """

    def wait(self):
        """
        禁止1天
        :return:
        """
        return 24*60*60

    def allow_request(self, request, view):
        """
        是否运行请求
        :param request:
        :param view:
        :return:
        """
        # 判断同一个手机号访问的次数
        if request.body is None:
            # 业务层的逻辑，不处理
            return True
        phone = json.loads(request.body).get('phone', None)
        if phone is None:
            return True

        tody_from_zero = str(datetime.datetime.now().date()) + '00:00'
        query_params = {
            'phone': phone,
            'send_time__gte': datetime.datetime.strptime(tody_from_zero, '%Y-%m-%d%H:%M'),
            'send_time__lte': datetime.datetime.now()
        }

        # 到目前位置一共发送了多少条信息
        phone_send = VerifyCode.objects.filter(**query_params)

        if phone_send.count() >= settings.MESSAGE_PHONE_LIMIT_COUNT:
            return self.throttle_failure()
        return True

    def throttle_failure(self):
        """
        禁止访问
        """
        class NewThrottled(exceptions.APIException):

            def __init__(self, detail=None, code=None):
                super().__init__(detail, code)

        raise NewThrottled(detail={'code': 10110, 'msg': '今日访问已达上线, 一天后才可以访问!'})






