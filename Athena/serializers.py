from django.contrib.auth.models import User, Group
from rest_framework import serializers

from Athena.models import Stock


class StockSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(required=True, max_length=10)
    date = serializers.DateField()
    open = serializers.FloatField()
    close = serializers.FloatField()
    zhang_die = serializers.FloatField()
    zhang_die_fu = serializers.CharField(max_length=20)
    highest = serializers.FloatField()
    lowest = serializers.FloatField()
    cheng_jiao_liang = serializers.IntegerField()
    cheng_jiao_e = serializers.FloatField()
    huan_shou_lv = serializers.CharField(max_length=10)

    def create(self, validated_data):
        return Stock.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.date = validated_data.get('date', instance.date)
        instance.open = validated_data.get('open', instance.open)
        instance.close = validated_data.get('close', instance.close)
        instance.zhang_die = validated_data.get('zhang_die', instance.zhang_die)
        instance.zhang_die_fu = validated_data.get('zhang_die_fu', instance.zhang_die_fu)
        instance.highest = validated_data.get('highest', instance.highest)
        instance.lowest = validated_data.get('lowest', instance.lowest)
        instance.cheng_jiao_liang = validated_data('cheng_jiao_liang', instance.cheng_jiao_liang)
        instance.cheng_jiao_e = validated_data('cheng_jiao_e', instance.cheng_jiao_e)
        instance.huan_shou_lv = validated_data('huan_shou_lv', instance.huan_shou_lv)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

