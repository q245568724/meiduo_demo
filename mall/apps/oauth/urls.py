from django.conf.urls import url
from .views import *
from oauth.views import OauthQQURLAPIView

urlpatterns =[
    url(r'qq/statues/$',OauthQQURLAPIView.as_view()),
    url(r'qq/users/$',OAuthQQUserAPIView.as_view()),
]