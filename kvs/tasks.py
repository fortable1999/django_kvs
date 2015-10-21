from __future__ import absolute_import

from celery import shared_task

@shared_task
def kvs_expires(key):
    try:
        from kvs.models import KeyValue
        obj = KeyValue.objects.get(key=key)
        return obj.expire()
    except:
        print("No key")
        return False

