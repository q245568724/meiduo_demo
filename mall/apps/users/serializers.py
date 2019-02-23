import re
from rest_framework import serializers
from django_redis import get_redis_connection
from users.models import User


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

        # 用户入库之后 我们生成token
        from rest_framework_jwt.settings import api_settings
        # 4.1 需要使用jwt的两个方法
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 4.2 让payload(载荷)盛放一些用户信息
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token=token

        return user

# class Person(object):
#     name='itcast'
#
# p = Person()
# p.name

