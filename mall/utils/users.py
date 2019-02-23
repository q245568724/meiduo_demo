def jwt_response_payload_handler(token, user=None, request=None):
    # token  jwt 生成的token
    # user=None, jwt验证成功之后的user
    # request=None  请求
    return {
        'token': token,
        'user_id': user.id,
        'username':user.username
    }