from django.urls import path
from.views import userRegistrationViewset

urlpatterns = [
    path('register/',userRegistrationViewset.as_view({'post':'create'}),name='register'),
]