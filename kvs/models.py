from django.db import models
from datetime import datetime, timedelta, timezone
from kvs.tasks import kvs_expires
from django.conf import settings

# Create your models here.

class KeyValueManager(models.Manager):

    def kv_update(self, key, value):
        try:
            obj = KeyValue.objects.get(key=key)
            print("KeyValue exist. update.")
        except:
            obj = KeyValue(key=key)
            print("KeyValue NOT exist. create.")
        obj.value = value

        expires_at = datetime.utcnow() + timedelta(
                seconds=settings.KV_EXIST_SECONDS
                )
        obj.expires_at = expires_at

        obj.save()
        kvs_expires.apply_async(
                args=[key],
                queue="djangokv",
                eta= expires_at
                )
        return True
        

class KeyValue(models.Model):

    key = models.CharField(max_length=40)
    value = models.CharField(max_length=40)
    expires_at = models.DateTimeField()

    objects = KeyValueManager()

    def is_expired(self):
        """docstring for is_expired"""
        return datetime.now(timezone.utc) > self.expires_at

    def expire(self):
        print("expire key: %s" % self.key)
        if self.is_expired():
            self.delete()
            return True
        return False

    def expire_force(self):
        self.delete()
        return True
