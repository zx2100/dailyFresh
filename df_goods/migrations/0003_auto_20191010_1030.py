# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0002_auto_20191001_2255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goodinfo',
            options={'verbose_name': '商品管理', 'verbose_name_plural': '商品管理'},
        ),
        migrations.AlterModelOptions(
            name='typeinfo',
            options={'verbose_name': '类型管理', 'verbose_name_plural': '类型管理'},
        ),
        migrations.AlterField(
            model_name='goodinfo',
            name='brief',
            field=models.CharField(verbose_name='商品简介', max_length=200),
        ),
        migrations.AlterField(
            model_name='goodinfo',
            name='click',
            field=models.IntegerField(verbose_name='点击量'),
        ),
        migrations.AlterField(
            model_name='goodinfo',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='商品描述'),
        ),
        migrations.AlterField(
            model_name='goodinfo',
            name='gtype',
            field=models.ForeignKey(verbose_name='商品分类', to='df_goods.TypeInfo'),
        ),
        migrations.AlterField(
            model_name='goodinfo',
            name='inventory',
            field=models.IntegerField(verbose_name='商品库存'),
        ),
        migrations.AlterField(
            model_name='goodinfo',
            name='isDelete',
            field=models.BooleanField(verbose_name='是否删除', default=False),
        ),
        migrations.AlterField(
            model_name='goodinfo',
            name='pic',
            field=models.ImageField(verbose_name='商品图片', upload_to='goods'),
        ),
        migrations.AlterField(
            model_name='goodinfo',
            name='price',
            field=models.DecimalField(verbose_name='商品价格', max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='goodinfo',
            name='title',
            field=models.CharField(verbose_name='商品名称', max_length=20),
        ),
        migrations.AlterField(
            model_name='goodinfo',
            name='unit',
            field=models.CharField(verbose_name='商品单位', max_length=20, default='500g'),
        ),
    ]
