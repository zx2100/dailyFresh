# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='商品名称', max_length=20)),
                ('pic', models.ImageField(verbose_name='商品图片', upload_to='goods')),
                ('price', models.DecimalField(verbose_name='商品价格', max_digits=5, decimal_places=2)),
                ('isDelete', models.BooleanField(verbose_name='是否删除', default=False)),
                ('unit', models.CharField(verbose_name='商品单位', max_length=20, default='500g')),
                ('click', models.IntegerField(verbose_name='点击量')),
                ('brief', models.CharField(verbose_name='商品简介', max_length=200)),
                ('inventory', models.IntegerField(verbose_name='商品库存')),
                ('content', ckeditor.fields.RichTextField(verbose_name='商品描述')),
                ('last_updated', models.BigIntegerField(default=1572599064)),
            ],
            options={
                'verbose_name': '商品管理',
                'verbose_name_plural': '商品管理',
            },
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=20, unique=True)),
                ('isDelete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '类型管理',
                'verbose_name_plural': '类型管理',
            },
        ),
        migrations.AddField(
            model_name='goodinfo',
            name='gtype',
            field=models.ForeignKey(verbose_name='商品分类', to='df_goods.TypeInfo'),
        ),
    ]
