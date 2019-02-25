from rest_framework import serializers

from oauth.models import OAuthQQUser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django_redis import get_redis_connection
from oauth.utils import check_access_token
from users.models import User
from users.utlis import redis_check_code


class OAuthQQUserSerializer(serializers.Serializer):
    """
        QQ登录创建用户序列化器
        """
    access_token = serializers.CharField(label='操作凭证')
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$')
    password = serializers.CharField(label='密码', max_length=20, min_length=8)
    sms_code = serializers.CharField(label='短信验证码')


    def validate(self, data):
        # 1 需要对加密的openid进行处理
        access_token = data['access_token']

        openid = check_access_token(access_token)

        if openid is None:
            raise serializers.ValidationError('openid错误')

        #  我们通过data来传递数据
        data['openid']=openid

        # 2 需要对短信进行验证
        mobile = data['mobile']
        sms_code = data['sms_code']
        # 2.1 检验短信验证码
        redis_check_code(mobile,sms_code)
        # 3 需要对手机号进行判断
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 说明没有注册过
            # 创建用户
            # User.objects.create():
            pass
        else:
            # 说明注册过
            # 注册过需要验证密码
            if not user.check_password(data['password']):
                raise serializers.ValidationError('密码不正确')
            data['user']=user

        return data
    # request.data --> 序列化器(data=xxx)
    # data --> attrs --> validated_data
    def create(self, validated_data):
        user = validated_data.get('user')

        if user is None:
            # 创建user
            user = User.objects.create(
                mobile=validated_data.get('mobile'),
                username=validated_data.get('mobile'),
                password=validated_data.get('password')
            )

        qquser = OAuthQQUser.objects.create(
            user=user,
            openid=validated_data.get('openid')
        )

        return qquser