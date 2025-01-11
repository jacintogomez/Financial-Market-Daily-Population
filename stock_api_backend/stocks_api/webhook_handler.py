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
    def send_webhook(cls,status,task_id,result=None,message=None,ratio=None,partial_errors=None):
        webhook_url=settings.WEBHOOK_URL
        if not webhook_url:
            return
        payload={
            'status':status,
            'task_id':task_id,
            'message':message or (cls.success_msg if status=='success' else cls.failure_msg),
        }
        if result is not None:
            payload['result']=result
        if ratio is not None:
            payload['ratio']=str(ratio)
        if partial_errors is not None:
            payload['partial_errors']=str(partial_errors)
        try:
            requests.post(webhook_url,json=payload)
        except Exception as e:
            print(f'Error sending webhook notification: {e}')

    def on_success(self,retval,task_id,args,kwargs):
        self.send_webhook(
            status='success',
            task_id=task_id,
            message=retval.get('message') if isinstance(retval,dict) else None,
            result={
                'ratio':retval.get('ratio') if isinstance(retval,dict) else None,
                'partial_errors': retval.get('partial_errors') if isinstance(retval,dict) else None
            },
        )

    def on_failure(self,exc,task_id,args,kwargs,einfo):
        self.send_webhook(
            status='failure',
            task_id=task_id,
            message=self.failure_msg,
            result=exc,
        )