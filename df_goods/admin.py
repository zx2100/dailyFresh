from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.TypeInfo)
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'isDelete']



@admin.register(models.GoodInfo)
class GoodInfoAdmin(admin.ModelAdmin):
    list_display = [
                'title',  'price', 'unit', 'click', 'inventory'
                , 'gtype', 'isDelete'
                ]


