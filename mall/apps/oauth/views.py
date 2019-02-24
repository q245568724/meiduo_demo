from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

"""
当用户点击qq按钮的时候,会发送一个请求,
我们后端返回给它一个url (URL是根据文档拼接出来的)

GET  /oauth/qq/status/


"""
class OauthQQURLAPIView(APIView):

    def get(self,request):

        auth_url = 'http://www.meiduo.site:8080/oauth_callback.html'

        return Response({"auth_url":auth_url})


