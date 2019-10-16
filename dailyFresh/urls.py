"""dailyFresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from df_goods.admin import goods_site

urlpatterns = [
    # 暂时用于商品管理
    url(r'^admin/', include(goods_site.urls)),
    url(r'^user/', include("df_user.urls", namespace="df_user")),
    # 专门用户商品管理
    # url(r'^goodsadmin/', include(goods_site.urls)),
    # 购物车url
    url(r'^cart/', include("df_cart.urls", namespace="df_cart")),
    url(r'^', include("df_goods.urls", namespace='df_goods'))
]

