from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime
import time
# Create your models here.


class Meta:
    verbose_name = '商品'


class TypeInfo(models.Model):
    title = models.CharField(max_length=20, unique=True)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '类型管理'
        verbose_name_plural = '类型管理'


class GoodInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='商品名称')
    pic = models.ImageField(upload_to='goods', verbose_name='商品图片')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='商品价格')
    # 逻辑删除
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')
    unit = models.CharField(max_length=20, default="500g", verbose_name='商品单位')
    click = models.IntegerField(verbose_name='点击量')
    brief = models.CharField(max_length=200, verbose_name='商品简介')
    inventory = models.IntegerField(verbose_name='商品库存')
    content = RichTextField(verbose_name='商品描述')
    gtype = models.ForeignKey(TypeInfo, verbose_name='商品分类')
    # Unix时间戳,程序更新时，应该自动更新
    last_updated = models.BigIntegerField(default=int(time.mktime(datetime.now().timetuple())))


    class Meta:
        verbose_name = '商品管理'
        verbose_name_plural = '商品管理'

    # 重写self方法，实现自动更新时间戳
    def save(self, *args, **kwargs):
        self.last_updated = int(time.mktime(datetime.now().timetuple()))
        super(GoodInfo, self).save(*args, **kwargs)
