import requests
from django.conf import settings
from celery import Task

class WebhookTask(Task):

    success_msg='Task completed successfully'
    failure_msg='Task failed'

    def __init__(self):
        self.success_msg='Task completed successfully'
        self.failure_msg='Task failed'

    def set_messages(self,success_msg=None,failure_msg=None):
        self.success_msg=success_msg
        self.failure_msg=failure_msg
        return self

    @classmethod
    def send_webhook(cls,status,task_id,message=None,result=None,error=None):
        webhook_url=settings.WEBHOOK_URL
        if not webhook_url:
            return
        payload={
            'status':status,
            'task_id':task_id,
            'message':message or {},
        }
        if result is not None:
            payload['result'] = result
        if error is not None:
            payload['error'] = str(error)
        try:
            requests.post(webhook_url,json=payload)
        except Exception as e:
            print(f'Error sending webhook notification: {e}')

    def on_success(self,retval,task_id,args,kwargs):
        self.send_webhook(
            status='success',
            task_id=task_id,
            message=self.success_msg,
            result=retval,
        )

    def on_failure(self,exc,task_id,args,kwargs,einfo):
        self.send_webhook(
            status='failure',
            task_id=task_id,
            message=f'{self.failure_msg}: {str(exc)}',
            result=exc,
        )