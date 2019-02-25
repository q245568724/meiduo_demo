from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
"""
1 根据需求自己定义模型
2 使用django自带的模型和认证系统

"""
class User(AbstractUser):
    # 面向对象通过继承父类模型添加字段
    mobile = models.CharField(max_length=11,unique=True,verbose_name='手机号')

    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
