from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^details$', views.detail, name='detail'),
    url(r'^list$', views.goods_list, name='goods_list'),

]
