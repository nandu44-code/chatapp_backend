from django.urls import path
from .views import UserRegistrationViewSet

urlpatterns = [
    path('register/',UserRegistrationViewSet.as_view({'post':'create'}),name='register'),
]