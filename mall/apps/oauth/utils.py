from rest_framework_jwt.settings import api_settings

def oauth_token(user):
    # 4.1 需要使用jwt的两个方法
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    # 4.2 让payload(载荷)盛放一些用户信息
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    return token