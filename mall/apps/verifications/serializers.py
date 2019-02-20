from rest_framework import serializers

class RegisterSmsSerializer(serializers.Serializer):

    text=serializers.CharField(max_length=4,min_length=4,required=True)
    image_code_id=serializers.UUIDField(required=True)

    """
    序列化器的验证:
    1 字段类型
    2 字段选项
    3 单个字段
    4 多个字段
    """

    def vaildate(self,attrs):
        # 1 获取用户提交的验证码
        text = attrs['text']
        image_id = attrs['image_code_id']
        # 2 获取redis的验证码
        # 3 对比