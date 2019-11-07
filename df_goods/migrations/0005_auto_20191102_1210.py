# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0004_auto_20191102_1209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goodinfo',
            name='last_update',
        ),
        migrations.AddField(
            model_name='goodinfo',
            name='last_updated',
            field=models.BigIntegerField(default=1572667808),
        ),
    ]
