# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0003_auto_20191102_1209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodinfo',
            old_name='last_updated',
            new_name='last_update',
        ),
    ]
