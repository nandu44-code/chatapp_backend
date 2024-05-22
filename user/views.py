from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
# Create your views here.

class userRegistrationViewset(ModelViewSet):

    queryset = CustomUser.objects.none() 
    serializer_class = UserRegistrationSerializer

    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()      

    