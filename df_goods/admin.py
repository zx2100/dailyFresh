# coding=utf8
from django.contrib import admin
from . import models


# Register your models here.
class GoodsAdminSite(admin.AdminSite):
    site_header = "dayFresh商品管理平台"
    site_title = "dayFresh商品管理平台"


goods_site = GoodsAdminSite(name="goodsAdmin")


@admin.register(models.TypeInfo, site=goods_site)
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'isDelete']


@admin.register(models.GoodInfo, site=goods_site)
class GoodInfoAdmin(admin.ModelAdmin):
    list_display = [
                'title',  'price', 'unit', 'click', 'inventory'
                , 'gtype', 'isDelete'
                ]
    list_per_page = 50
    list_filter = ("gtype", "isDelete")

