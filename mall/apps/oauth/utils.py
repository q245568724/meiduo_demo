from rest_framework_jwt.settings import api_settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from mall import settings

def generate_token(user):
    # 4.1 需要使用jwt的两个方法
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    # 4.2 让payload(载荷)盛放一些用户信息
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    return token


def generic_open_id(openid):
    # 1 创建序列化器
    s = Serializer(secret_key=settings.SECRET_KEY,expires_in=60*60)
    # 2 对数据进行处理
    token = s.dumps({
        'openid':openid
    })
    # 3 返回
    return token.decode()