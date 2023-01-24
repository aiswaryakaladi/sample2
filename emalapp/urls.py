from django.urls import path
from .views import *

urlpatterns=[
     path('reg/',reg),
     path('emailsend/',emailsend),
     path('login/',login),
     path('verify/<auth_token>',verify),
     path('loginpage/',loginpage),
]
