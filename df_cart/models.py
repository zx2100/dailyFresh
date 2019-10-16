#coding="utf-8"

from django.db import models
from df_user.models import UserInfo
from df_goods.models import GoodInfo

# Create your models here.

class CartInfo(models.Model):
    goods = models.ForeignKey(GoodInfo)
    count = models.IntegerField()
    user = models.ForeignKey(UserInfo)