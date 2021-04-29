
from rest_framework import (
    routers)
from django.conf.urls import url, include
from .views import *
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register(r'item', itemViewSet)
# router.register(r'bid', bidViewSet)
# router.register(r'auditLog', auditLogViewSet)
# router.register(r'userreg', UserViewSet)
router.register('userplug1/OrganizationPicture',
                BookUpdateImageAPIView, 'CODE')
urlpatterns = [
    url(r'^userreg/$', UserView.as_view()),
    url(r'^user/$', UserDetailView.as_view()),
    url(r'^userchangepwd/$', UserchangePWView.as_view()),
    url(r'^userplug1/$', UserplugView.as_view()),  # 获取用户扩展信息



    url(r'^', include(router.urls)),
]
