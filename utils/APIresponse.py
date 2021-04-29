from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, code=200, message='success', data=None, status=None, headers=None, content_type=None, **kwargs):
        dic = {'code': code, 'message': message}
        if data:
            dic['data'] = data
        else:
            dic['code'] = 1
            dic['message'] = "操作失败"

        dic.update(kwargs)  # 这里使用update更新
        super().__init__(data=dic, status=status,
                         template_name=None, headers=headers,
                         exception=False, content_type=content_type)
