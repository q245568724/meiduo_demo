"""
1 创建任务
2 创建celery实例
3 在celery中 设置任务, broker
4 worker

"""

# 任务就是普通的函数
# 1 这个普通的函数 必须要被celery实例对象的 task装饰器装饰
# 2 这个任务需要celery自己检测
from libs.yuntongxun.sms import CCP
from celery_tasks.main import app

@app.task
def send_sms_code(mobile,sms_code):

    CCP().send_template_sms(mobile, [sms_code, 5], '1')
