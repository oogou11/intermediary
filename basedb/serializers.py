from rest_framework import serializers
import re

from .models import *


class CreateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)  # 'true'
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User  # 从User模型中映射序列化器字段
        # fields = '__all__'
        fields = ['id', 'username', 'password', 'password2',
                  'customer_type', 'email', 'contacts', 'cardid',
                  'phone', 'sms_code', 'allow', 'token']
        extra_kwargs = {  # 修改字段选项
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {  # 自定义校验出错后的错误信息提示
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_customertype(self, value):
        """单独校验用户类型"""
        if not value in ["1", "2"]:
            raise serializers.ValidationError('用户类型错误')
        return value

    def validate_phone(self, value):
        """单独校验手机号"""
        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式有误')
        return value

    def validate_allow(self, value):
        """是否同意协议校验"""
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate(self, attrs):
        """校验密码两个是否相同"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两个密码不一致')

        # # 校验验证码
        # redis_conn = get_redis_connection('verify_codes')
        # mobile = attrs['mobile']
        # real_sms_code = redis_conn.get('sms_%s' % mobile)
        # 向redis存储数据时都是以字条串进行存储的,取出来后都是bytes类型 [bytes]

        # if real_sms_code is None or attrs['sms_code'] != real_sms_code.decode():
        #     raise serializers.ValidationError('验证码错误')

        return attrs

    def create(self, validated_data):
        # 把不需要存储的 password2, sms_code, allow 从字段中移除
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']
        # 把密码先取出来
        password = validated_data.pop('password')
        # 创建用户模型对象, 给模型中的 username和mobile属性赋值

        user = User(**validated_data)

        user.set_password(password)  # 把密码加密后再赋值给user的password属性
        user.save()  # 存储到数据库

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username',
                  'customer_type', 'statustype', 'email', 'contacts', 'cardid',
                  'phone', ]


class UserchangePWSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='确认密码', write_only=True)

    class Meta:
        model = User
        fields = ['id', 'password2', 'password', ]
        extra_kwargs = {  # 修改字段选项
            'password': {
                'write_only': True
            },
        }

    def validate(self, attrs):

        if not self.instance.check_password(attrs['password']):
            raise serializers.ValidationError('原始密码错误')
        if attrs['password'] == attrs['password2']:
            raise serializers.ValidationError('两个密码一致')
        return attrs

    def update(self, instance, validated_data):

        pwd = validated_data.pop('password2')

        instance.set_password(pwd)
        validated_data['password'] = instance.password
        return super().update(instance, validated_data)


class User1Serializer(serializers.ModelSerializer):
    class Meta:
        model = ProprietorProfile
        fields = ['organization_code', 'organization_picture', 'organization_name']

    def create(self, validated_data):
        print(self)
        validated_data['user'] = self.context['request'].user
        pp = ProprietorProfile.objects.filter(user=validated_data['user'])
        if pp.exists():

            return super().update(pp[0], validated_data)
        else:
            return super().create(validated_data)


class BookUpdateImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProprietorProfile
        fields = ['organization_picture']
