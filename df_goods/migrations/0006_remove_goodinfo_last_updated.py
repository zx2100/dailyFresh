# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0005_auto_20191102_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goodinfo',
            name='last_updated',
        ),
    ]
