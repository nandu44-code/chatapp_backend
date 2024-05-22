from rest_framework.serializers import ModelSerializer
from .models import CustomUser
from .views import userRegistrationViewset

class userRegistrationSerilaizer(ModelSetializer):

    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
