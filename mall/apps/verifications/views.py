import random

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from libs.captcha.captcha import captcha
from libs.yuntongxun.sms import CCP
from verifications.serializers import RegisterSmsSerializer

"""
前端传递一个uuid,我们生成一个图片

1 接受 image_code_id
2 生成图片和验证码
3 把验证码保存到redis中
4 返回图片响应

GET /verifications/images/(?P<image_code_id?)/

"""

class RegisterImageAPIView(APIView):

    def get(self, request, image_code_id):
        # 1 接受 image_code_id
        # 2 生成图片和验证码
        text,image = captcha.generate_captcha()
        # 3 把验证码保存到redis中
        # 链接redis
        redis_conn = get_redis_connection('code')
        # 设置图片
        redis_conn.setex('img_%s'%image_code_id,60,text)
        # 4 返回图片响应
        return HttpResponse(image,content_type='image/jpeg')
        # return Response()


"""
用户点击获取短信按钮的时候,前段应该将手机号,图片验证码以及验证码id发送给后端

1 接受参数
2 校验参数
3 生成短信
4 将短信保存在redis中
5 使用云通讯发送短信
6 返回响应

GET     verifications/smscodes/(?P<mobile>1[3-9]\d{9})/?text=xxxx&image_code_id=xxxx
        werther/2018/?place=beijing
"""

class RegisterSmscodeAPIView(APIView):

    def get(self,request,mobile):
        # 1 接受参数
        params = request.query_params
        # 2 校验参数,还要验证码用户输入的图片验证码和redis的保存是否一致
        serializer = RegisterSmsSerializer(data=params)
        serializer.is_valid(raise_exception=True)
        # 3 生成短信
        sms_code = '%06d'%random.randint(0,999999)
        # 4 将短信保存在redis中
        redis_conn =get_redis_connection('code')
        redis_conn.setex('sms_'+mobile,5*60,sms_code)
        # 5 使用云通讯发送短信
        CCP().send_template_sms(mobile,[sms_code,5],'1')
        # 6 返回响应
        return Response({'msg':'ok'})

