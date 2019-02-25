from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from QQLoginTool.QQtool import OAuthQQ

from rest_framework import status
from rest_framework.settings import api_settings
from mall import settings
from oauth.models import OAuthQQUser
from oauth.serializers import OAuthQQUserSerializer
from oauth.utils import  generate_token, generic_open_id

"""
当用户点击qq按钮的时候,会发送一个请求,
我们后端返回给它一个url (URL是根据文档拼接出来的)

GET  /oauth/qq/status/


"""
class OauthQQURLAPIView(APIView):

    def get(self,request):

        # auth_url = 'http://www.meiduo.site:8080/oauth_callback.html'
        state = '/'
        # 1 创建oauth对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=state,
                        )
        # 2 获取跳转的url
        auth_url = oauth.get_qq_url()

        return Response({"auth_url":auth_url})

"""
1 用户同意授权登陆,这个时候会返回一个code
2 我们用code换取token
3 有了token,我们在获取openid

"""
"""
前端会接收到用户同意之后的code,前端应该将这个code发送给后端
 1 接受这个数据
 2 用code换token
 3 用token换openid

GET    /oauth/qq/user/?code=xxxxx
"""
class OAuthQQUserAPIView(APIView):

    def get(self,request):
        # 1 接受这个数据
        params = request.query_params
        code = params.get('code')
        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # 2 用code换token
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,)
        token = oauth.get_access_token(code)
        # 3 用token换openid
        openid = oauth.get_open_id(token)
        # 获取的openid有两种情况:
        # 1 用户之前绑定过
        # 2 用户之前没有绑定过
        # 根据openid查询数据库
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 不存在
            # 返回openid让用户在前端进行绑定
            # openid 很重要,所以我们需要对openid进行加密
            # 绑定也应该有一个时效
            token = generic_open_id(openid)
            return Response({'access_token':token})
        else:
            # 生成token
            token = generate_token(qquser.user)

            return Response({
                'token':token,
                'username':qquser.user.username,
                'user_id':qquser.user.id})


    def post(self,request):
        # 1 接受数据
        data = request.data
        # 2 校验数据
        serializer = OAuthQQUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # 3 数据入库
        qquser = serializer.save()
        # 4 返回响应,应该有token数据
        token = generate_token(qquser.user)
        return Response({
            'token':token,
            'username':qquser.user.username,
            'user_id':qquser.user.id
        })

"""
当用户点击绑定的时候,我们需要将手机号,密码,短信验证码和加密的openid传递过来

1 接受数据
2 校验数据
3 数据入库
4 返回响应

POST
"""
