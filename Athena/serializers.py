from django.contrib.auth.models import User, Group
from rest_framework import serializers

from Athena.models import StockInfo


class StockInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInfo
        # fields = ('id', 'code',)
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

