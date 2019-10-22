# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0003_auto_20191010_1030'),
        ('df_user', '0002_auto_20190923_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetailInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('count', models.IntegerField()),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('subtotal', models.IntegerField()),
                ('pic', models.ImageField(upload_to='order/goods')),
                ('title', models.CharField(max_length=20)),
                ('unit', models.CharField(max_length=20, default='500g')),
                ('goods', models.ForeignKey(to='df_goods.GoodInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateField(auto_now=True)),
                ('address', models.CharField(max_length=100)),
                ('consignee', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=30)),
                ('payment_status', models.BooleanField(default=False)),
                ('payment', models.DecimalField(max_digits=8, decimal_places=2)),
                ('another_id', models.BigIntegerField(unique=True)),
                ('user', models.ForeignKey(to='df_user.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='order',
            field=models.ForeignKey(to='df_order.OrderInfo'),
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='order_aff',
            field=models.ForeignKey(related_name='order_aff', to='df_order.OrderInfo', to_field='another_id'),
        ),
    ]
