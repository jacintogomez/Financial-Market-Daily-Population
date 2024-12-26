import requests
from django.conf import settings
from celery import Task

class WebhookTask(Task):

    default_success_msg='Task completed successfully'
    default_failure_msg='Task failed'

    def __init__(self):
        self.success_msg=None
        self.failure_msg=None

    def set_messages(self,success_msg=None,failure_msg=None):
        self.success_msg=success_msg
        self.failure_msg=failure_msg
        return self

    def on_success(self,retval,task_id,args,kwargs):
        webhook_url=settings.WEBHOOK_URL
        if webhook_url:
            payload={
                'status':'success',
                'task_id':task_id,
                'result':retval,
                'task_name':self.name,
                'message':self.success_msg or self.default_success_msg
            }
            try:
                requests.post(webhook_url,json=payload)
            except requests.RequestException as e:
                print(f'Failed to send webhook notification: {e}')

    def on_failure(self,exc,task_id,args,kwargs,einfo):
        webhook_url=settings.WEBHOOK_URL
        if webhook_url:
            payload={
                'status':'failure',
                'task_id':task_id,
                'error':str(exc),
                'task_name':self.name,
                'message':self.failure_msg or self.default_failure_msg
            }
            try:
                requests.post(webhook_url,json=payload)
            except requests.RequestException as e:
                print(f'Failed to send webhook notification: {e}')