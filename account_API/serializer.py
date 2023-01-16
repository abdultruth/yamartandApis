from account.models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'url', 'phone_no', 'email', 'first_name', 'last_name', 'is_staff']
    