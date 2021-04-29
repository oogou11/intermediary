# from intermediary import utils
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets,  pagination
from .serializers import NewsClassSerializer, NewsSerializer, SinglePageSerializer
from .models import *
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from utils.APIresponse import APIResponse
from rest_framework_simplejwt.authentication import JWTAuthentication


class PageSet(pagination.PageNumberPagination):
    # 每页显示多少个
    page_size = 10
    # 默认每页显示3个
    page_size_query_param = "size"
    # 最大页数
    max_page_size = 50
    # 获取页码数的
    page_query_param = 'page'


class NewsClassViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    retrieve:
        Return a user instance.
    list:
        文章分类接口
    create:
        Create a new user.
    delete:
        Remove an existing user.
    partial_update:
        Update one or more fields on an existing user.
    update:
        Update a user.
    """
    serializer_class = NewsClassSerializer
    queryset = NewsClass.objects.all()
    # queryset = NewsClass.objects.filter(NewsClassId=1)
    authentication_classes = [JWTAuthentication]
    permission_classes = []
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('NewsClassId', 'id', 'group')

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        # print(request['partner'])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            # return APIResponse(code=0, message='查询成功', result=self.get_paginated_response(serializer.data),)
            return Response({'code': 200, 'msg': 'success',
                             'count': queryset.count(),
                             'data': serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        # return APIResponse(code=0, message='查询成功', result=serializer.data,)
        return Response({'code': 200, 'msg': 'success',
                         'count': queryset.count(),
                         'data': serializer.data})


class NewsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    retrieve:
        文章详情接口
    list:
        文章列表接口
    """
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    authentication_classes = []  # (JWTAuthentication, )
    permission_classes = []
    pagination_class = PageSet
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ('NewsClass', )
    ordering_fields = ('in_num',)

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(serializer.data['id'])
        News.objects.filter(id=serializer.data['id']).update(
            in_num=F('in_num') + 1)

        # return APIResponse(code=0, message='查询成功', result=serializer.data,)
        return Response({'code': 200, 'msg': 'success',
                         'data': serializer.data})

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        # print(request['partner'])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # return self.get_paginated_response(serializer.data)
            return Response({'code': 200, 'msg': 'success', 'count': queryset.count(), 'data': serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        # return APIResponse(code=0, message='查询成功', result=serializer.data,)
        return Response({'code': 200, 'msg': 'success', 'count': queryset.count(), 'data': serializer.data})


class SinglePageViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    retrieve:
        单页详情接口
    list:
        单页列表接口
    """
    serializer_class = SinglePageSerializer
    queryset = SinglePage.objects.all()
    authentication_classes = []  # (JWTAuthentication, )
    permission_classes = []
    # pagination_class = PageSet
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('code',)

    def retrieve(self, request, *args, **kwargs):

        try:
            instance = self.get_object()  # 用get需要加 try。否则一旦没数据就会抛出异常
        except Exception as ex:
            return Response({'code': 10116, 'msg': '数据不存在'})
        serializer = self.get_serializer(instance)
        print(serializer.data['id'])
        SinglePage.objects.filter(id=serializer.data['id']).update(
            in_num=F('in_num') + 1)

        # return Response(ret.get_data)
        # return APIResponse(code=0, message='查询成功', result=serializer.data,)
        return Response({'code': 200, 'msg': 'success',
                         'data': serializer.data})

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        # print(request['partner'])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # return self.get_paginated_response(serializer.data)
            return Response({'code': 200, 'msg': 'success',
                             'count': queryset.count(),
                             'data': serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
        # return Response(serializer.data)
        # return APIResponse(code=0, message='查询成功', result=serializer.data,)
        return Response({'code': 200, 'msg': 'success',
                         'count': queryset.count(),
                         'data': serializer.data})
