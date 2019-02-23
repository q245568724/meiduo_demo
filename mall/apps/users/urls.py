from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.RegisterUsernameAPIView.as_view()),
    url(r'^$', views.RegiserUserAPIView.as_view()),
    # 实现登陆
    url(r'^auths/',obtain_jwt_token),
]