from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import RegiserUserSerializer
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
        #
        return Response({'count':count,'username':username})

"""
用户点击注册按钮的时候 前段需要收集 手机号,用户名,密码,短信验证码,确认密码,是否同意协议

1 接受数据
2 校验数据
3 数据入库
4 返回响应

POST    /users/register/


"""
# from rest_framework import
class RegiserUserAPIView(APIView):

    def post(self,request):
        # 1 接受数据
        data = request.data
        # 2 校验数据
        serializer = RegiserUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # 3 数据入库
        serializer.save()
        # 4 返回响应
        return Response(serializer.data)
