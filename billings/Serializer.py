from rest_framework import serializers


class CreateAccountSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    meter_number = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField()
    password = serializers.CharField()


class MakeBillSerializer(serializers.Serializer):
    volume = serializers.IntegerField()


