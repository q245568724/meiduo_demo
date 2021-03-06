import re
from rest_framework import serializers
from django_redis import get_redis_connection

# from oauth.utils import oauth_token
from rest_framework.views import APIView

from mall import settings
from oauth.utils import generate_token
from users.models import User
from users.utils import generic_verify_url


class RegiserUserSerializer(serializers.ModelSerializer):

    """
    ModelSerializer
    会对fields 进行遍历, 先去mobel中查看是否有相应的字段
    如果有 则自动生成
    如果没有 则查看当前类是否有定义
    """
    password2 = serializers.CharField(label='校验密码', allow_null=False, allow_blank=False, write_only=True)
    sms_code = serializers.CharField(label='短信验证码',write_only=True, max_length=6, min_length=6, allow_null=False, allow_blank=False)
    allow = serializers.CharField(label='是否同意协议', allow_null=False, allow_blank=False, write_only=True)

    token = serializers.CharField(label='token',read_only=True)

    class Meta:
        model = User
        fields = ['id','mobile','username','password','sms_code','allow','password2','token']

        extra_kwargs = {
            'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            },
        }
    """
    校验数据
    1 字段类型
    2 字段选项
    3 单个字段
    4 多个字段

    mobile: 符合手机规则
    allow:是否同意协议
    两次密码需要一致

    """

    def zalidate_mobile(self,value):

        if not re.match(r'1[3-9]\d{9}',value):
            raise serializers.ValidationError('手机号不符合规则')

        return value

    def validate_allow(self,value):

        if value != 'true':
            raise serializers.ValidationError('没有同意协议')

        return value

    #多个字段
    def validate(self, attrs):
        # 两次密码需要一致
        password = attrs['password']
        password2 = attrs['password2']

        if password != password2:
            raise serializers.ValidationError('密码不一致')
        # 2 短信
        # 2.1 获取用户提交的
        sms_code = attrs['sms_code']
        mobile = attrs['mobile']
        # 2.2 获取redis
        redis_conn = get_redis_connection('code')
        redis_code = redis_conn.get('sms_%s'%mobile)
        if redis_code is None:
            raise serializers.ValidationError('短信验证码已过期')
        # 删除短信
        redis_conn.delete('sms_'+mobile)
        # 2.3 对比
        if sms_code != redis_code.decode():
            raise serializers.ValidationError('验证码不一致')

        return attrs

    def create(self, validated_data):
        print(validated_data)

        del validated_data['sms_code']
        del validated_data['allow']
        del validated_data['password2']
        # 1 自己把数据入库
        # user = User.objects.create(**validated_data)
        # 2  现在的数据满足要求了 可以让父类执行
        user = super().create(validated_data)
        # 3 密码还是明文
        # 我们需要加密
        user.set_password(validated_data['password'])
        user.save()
        # 生成token
        token = generate_token(user)

        user.token=token

        return user

# class Person(object):
#     name='itcast'
#
# p = Person()
# p.name


class UserCenterInfoSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化器
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'email_active')


class UserEmailInfoSerializer(serializers.ModelSerializer):
    """
    邮箱序列化器
    """
    class Meta:
        model = User
        fields = ('id', 'email')
        extra_kwargs = {
            'email': {
                'required': True
            }
        }

    def update(self, instance, validated_data):

        # 先把数据更新一下
        email = validated_data.get('email')

        instance.email=email
        instance.save()
        from django.core.mail import send_mail
        # subject            主题
        subject = '美多商场激活邮件'
        # message,          内容
        message = ''
        # from_email,       谁发送的
        from_email = settings.EMAIL_FROM
        # recipient_list,   收件人列表
        recipient_list = [email]

        # user_id = 8
        verify_url = generic_verify_url(instance.id)
        from celery_tasks.mail.tasks import send_celery_email
        send_celery_email.delay(subject,
                                message,
                                from_email,
                                email,
                                verify_url,
                                recipient_list)

        return instance
