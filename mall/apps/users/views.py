from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import RegiserUserSerializer, UserCenterInfoSerializer, UserEmailInfoSerializer
from users.utils import check_token
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

"""
个人中心的信息展示

1 让前端传递用户信息
2 根据用户信息来获取user
3 将对象转换为字典数据

GET    /users/infos/

"""
from rest_framework.permissions import IsAuthenticated
# class UserCenterInfoAPIView(APIView):
#
#     permission_classes = [IsAuthenticated]
#
#     def get(self,request):
#         # 1 获取用户信息
#         user = request.user
#         # 2 将模型转换为(JSON)
#         serializer = UserCenterInfoSerializer(user)
#         # 3 返回响应
#         return Response(serializer.data)
from rest_framework.generics import RetrieveAPIView
class UserCenterInfoAPIView(RetrieveAPIView):

    serializer_class = UserCenterInfoSerializer

    # queryset = User.objects.all()
    # 已有的父类不能满足我们的需求
    def get_object(self):

        return self.request.user


"""
当用户输入邮箱之后,点击保存的时候,
1 我们需要将邮箱内容发送给后端,后端需要更新制定用户的email字段
2 同时后端需要给这个邮箱发送一个激活链接
3 当用户点击链接的时候,改变email_active的状态

1 后端接收邮箱
2 校验
3 更新数据
4 返回响应

PUT    /users/emails/
"""
# class UserEmailInfoAPIView(APIView):
#
#     permission_classes = [IsAuthenticated]
#
#     def put(self,request):
#         # 1 后端接收邮箱
#         data = request.data
#         # 2 校验
#         serializer = UserEmailInfoSerializer(instance=request.user,data=data)
#         serializer.is_valid(raise_exception=True)
#         # 3 更新数据
#         serializer.save()
#         # 4 返回响应
#         return Response(serializer.data)
from rest_framework.generics import UpdateAPIView
class UserEmailInfoAPIView(UpdateAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = UserEmailInfoSerializer

    def get_object(self):

        return self.request.user


"""
激活需求:
当用户点击激活连接的时候,需要让前段接收到token信息
然后让前段发送一个请求,这个请求包含token信息

1 接受token信息
2 对token进行解析
3 解析获取user_id之后,进行查询
4 修改状态
5 返回响应

GET    /users/emails/verification/


"""

class UserEmailVerificationAPIView(APIView):

    def get(self,request):
        # 1 接受token信息
        token = request.query_params.get('token')
        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # 2 对token进行解析
        user_id = check_token(token)
        if user_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # 3 解析获取user_id之后,进行查询
        user = User.objects.get(pk=user_id)
        # 4 修改状态
        user.email_active=True
        # 5 返回响应
        return Response({'msg':'ok'})

