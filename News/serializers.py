from rest_framework import serializers
from .models import *


class NewsClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsClass
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class SinglePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SinglePage
        fields = "__all__"
