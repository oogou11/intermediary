from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from pickle import PUT
from requests.api import put
from uritemplate.api import partial
from .serializers import *
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from .models import User
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
#


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 用户自定义jwt字段
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # 增加明文token返回字段
        data['username'] = self.user.username
        data['groups'] = self.user.groups.values_list('name', flat=True)
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 增加密文解析后字段
        token['status'] = user.statustype
        # ...
        print(token)
        return token

# 自定义获取tokenvue，，urls.py需要重新指向


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# 自定义用户认证，支持用户名，手机号同是登陆


class MyCustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(phone=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IsyzPermission(permissions.BasePermission):
    message = '必须是业主才能访问'

    def has_permission(self, request, view):
        print(request.user)
        if request.user.customertype == "1":
            return True
        return False


class IszjPermission(permissions.BasePermission):
    message = '必须是中介机构才能访问'

    def has_permission(self, request, view):
        if request.user.customertype == "2":
            return True
        return False


class IsPassPermission(permissions.BasePermission):
    message = '账户审核未通过'

    def has_permission(self, request, view):
        return request.user.is_pass


class IsPassPermission(permissions.BasePermission):
    message = '审核通过后不可修改'

    def has_permission(self, request, view):
        return not request.user.is_pass


class UserView(CreateAPIView):
    '''用户注册'''
    serializer_class = CreateUserSerializer
    authentication_classes = []  # (JWTAuthentication, )
    permission_classes = []


class UserDetailView(RetrieveAPIView):
    """用户详细信息展示"""
    serializer_class = UserDetailSerializer
    # authentication_classes = [JWTAuthentication, ]
    # queryset = User.objects.all()
    permission_classes = [IsAuthenticated]  # 指定权限,只有通过认证的用户才能访问当前视图

    def get_object(self):
        """重写此方法返回 要展示的用户模型对象"""
        return self.request.user


class UserchangePWView(UpdateAPIView):
    """用户密码修改"""
    permission_classes = [IszjPermission,
                          IsAuthenticated, ]  # 指定权限,只有通过认证的用户才能访问当前视图

    serializer_class = UserchangePWSerializer
    queryset = User.objects.all()

    def get_object(self):
        """重写此方法返回 要展示的用户模型对象"""
        return self.request.user


class UserplugView(UpdateAPIView, CreateAPIView):
    """业主资料提交"""
    serializer_class = User1Serializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,
                          IsyzPermission]  # 指定权限,只有通过认证的用户才能访问当前视图

    def get_object(self):
        """重写此方法返回 要展示的用户模型对象"""
        return self.request.user


class BookUpdateImageAPIView(GenericViewSet, mixins.UpdateModelMixin):
    queryset = ProprietorProfile.objects.all()
    serializer_class = BookUpdateImageModelSerializer
