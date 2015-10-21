# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('kvs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyvalue',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 21, 5, 57, 33, 675765, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
