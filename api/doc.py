from rest_framework import viewsets
from rest_framework.response import Response
from .serializer import ServeTypeSerializers
from rest_framework.decorators import action
from basedb.models import ServeType


class TestViewSet(viewsets.ModelViewSet):
    queryset = ServeType.objects.all()
    serializer_class = ServeTypeSerializers

    @action(detail=True, methods=['get'])
    def get_list(self, request):
        recent_users = ServeType.objects.all()
        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)
