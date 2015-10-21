from django.shortcuts import render
from django.views.generic import View
from kvs.models import KeyValue
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from kvs.tasks import kvs_expires
from datetime import datetime, timedelta

# Create your views here.

class KeyValueView(View):

    def get(self, request, *args, **kwargs):
        key = kwargs.get('key')
        obj = get_object_or_404(KeyValue, key=key)
        return HttpResponse(obj.value)

    def post(self, request, *args, **kwargs):
        key = kwargs.get('key')
        value = request.body.decode('utf-8')
        KeyValue.objects.kv_update(key, value)
        return HttpResponse("OK")

    def delete(self, request, *args, **kwargs):
        key = kwargs.get('key')
        obj = get_object_or_404(KeyValue, key=key)
        obj.expire_force()
        return HttpResponse("OK")


class KeyValueManageView(View):

    def get(self, request, *args, **kwargs):
        kv_amount = KeyValue.objects.count()
        return HttpResponse(kv_amount)
        
