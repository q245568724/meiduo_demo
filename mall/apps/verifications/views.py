from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from django_redis import get_redis_connection
from libs.captcha.captcha import captcha

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
        redis_conn.setex('img_'+image_code_id,60,text)
        # 4 返回图片响应
        return HttpResponse(image,content_type='image/jpeg')
        # return Response()
