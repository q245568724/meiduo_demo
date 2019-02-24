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

