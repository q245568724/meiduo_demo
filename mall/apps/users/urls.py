from django.conf.urls import url

from users.views import *
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.RegisterUsernameAPIView.as_view()),
    url(r'^$', views.RegiserUserAPIView.as_view()),
    # 实现登陆
    url(r'^auths/',obtain_jwt_token),
    # jwt把用户名和密码给系统,让系统进行认证,认证成功之后jwt生成token
    url(r'^infos/', UserCenterInfoAPIView.as_view()),
    url(r'^emails/$',UserEmailInfoAPIView.as_view()),
    url(r'^emails/verification/$',UserEmailVerificationAPIView.as_view()),
]