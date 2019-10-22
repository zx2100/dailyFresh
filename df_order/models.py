# -*- coding: utf-8 -*-
from django.db import models
from df_goods.models import GoodInfo
from df_user.models import UserInfo

# Create your models here.


class OrderInfo(models.Model):
    # 订单日期
    date = models.DateField(auto_now=True)
    # 订单收货地址
    address = models.CharField(max_length=100)
    # 订单收货人
    consignee = models.CharField(max_length=20)
    # 收获人联系方式
    phone = models.CharField(max_length=20)
    # 订单状态
    status = models.CharField(max_length=30)
    # 谁的订单
    user = models.ForeignKey(UserInfo)
    # 是否已经付款
    payment_status = models.BooleanField(default=False)
    # 付款总额
    payment = models.DecimalField(max_digits=8, decimal_places=2)
    # 订单编号
    another_id = models.BigIntegerField(unique=True)


class OrderDetailInfo(models.Model):
    # 订单归属
    order = models.ForeignKey(OrderInfo)
    # 所属订单信息,
    # order_aff = models.ForeignKey(OrderInfo, related_name="order_aff",to_field="another_id")
    order_aff = models.BigIntegerField()
    # 商品
    goods = models.ForeignKey(GoodInfo)
    # 数量
    count = models.IntegerField()
    # 拍下时的单价
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # 当前商品合计
    subtotal = models.IntegerField()
    # 拍下时的图片
    pic = models.ImageField(upload_to='order/goods')
    # 拍下时的名字
    title = models.CharField(max_length=20)
    # 拍下时的单位
    unit = models.CharField(max_length=20, default="500g")