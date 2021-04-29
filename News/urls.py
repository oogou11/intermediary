
from rest_framework import (
    routers)
from django.conf.urls import url, include
from .views import *

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'newsClass', NewsClassViewSet)
router.register(r'news', NewsViewSet)
router.register(r'singlepage', SinglePageViewSet)
urlpatterns = [

    url(r'^', include(router.urls)),
]
