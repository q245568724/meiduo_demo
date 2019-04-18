from base64 import decode

from django_redis import get_redis_connection

from rest_framework import serializers


def redis_check_code(mobile,sms_code):
    redis_conn = get_redis_connection('code')
    # 2.1 获取redis 数据
    redis_code = redis_conn.get('sms_' + mobile)
    if redis_code is None:
        raise serializers.ValidationError('短信验证码已过期')
    # 最好删除短信
    redis_conn.delete('sms_' + mobile)
    # 2.2 对比
    if redis_code.decode() != sms_code:
        raise serializers.ValidationError('验证码不一致')


from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature
from mall import settings
def generic_verify_url(user_id=None):

    # 1 创建序列化器
    s = Serializer(secret_key=settings.SECRET_KEY,expires_in=3600)
    # 2 组织数据
    data = {
        'id':user_id
    }
    # 3 对数据加密
    token = s.dumps(data)
    # 4 拼接url
    return 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token.decode()

def check_token(token):

    # 1 创建序列化器
    s = Serializer(secret_key=settings.SECRET_KEY,expires_in=3600)
    # 2 解析数据
    try:
        result = s.loads(token)
    except BadSignature:
        return None
    # 3 返回user_id
    return result.get('id')