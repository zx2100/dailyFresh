# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0002_auto_20191102_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodinfo',
            name='last_updated',
            field=models.BigIntegerField(),
        ),
    ]
