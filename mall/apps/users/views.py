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
        # 序列化: 将模型转换为JSON
        # 如何序列化的呢? 我们的序列化器是根据字段来查询模型中的对应字典,如果序列化中有,模型没有,则会报错
        # 如果字段设置为write_only 则会在序列化中忽略此字段
        return Response(serializer.data)


"""
当用户注册成功之后,自动登陆

自动登陆的功能 是要求 用户注册成功之后 返回数据的时候
需要额外添加一个 token

1 序列化的时候 添加token
2 token 怎么生成

"""