from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User

"""
前端发送用户给后端 我们后端判断用户名 是否注册
请求方式
GET   /users/usernames/(?P<username>\w{5,20})/count/

POST
"""

class RegisterUsernameAPIView(APIView):

    def get(self,request,username):
        # 判断用户是否注册
        # 查询用户名的数量,0就是没有注册,1就是有注册
        count = User.objects.filter(username=username).count()

        return Response({'count':count})