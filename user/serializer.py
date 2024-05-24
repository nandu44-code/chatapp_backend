from rest_framework import serializers 
from .models import CustomUser
from django.contrib.auth.models import Group,Permission


class UserRegistrationSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    user_permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        user_permissions_data = validated_data.pop('user_permissions', [])
        user = CustomUser.objects.create_user(**validated_data)
        user.groups.set(groups_data)
        user.user_permissions.set(user_permissions_data)

        return user