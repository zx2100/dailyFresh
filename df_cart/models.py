from django.db import models
from df_user.models import UserInfo
from df_goods.models import GoodInfo

# Create your models here.

class CartInfo(models.Model):
    goodsId = models.ForeignKey(UserInfo)
    count = models.IntegerField()
    uId = models.ForeignKey(GoodInfo)