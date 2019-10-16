from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r"^$", views.index, name='index'),
    url(r"^add$", views.add_to_cart, name='add'),
    url(r"^del$", views.del_from_cart, name='del'),
    url(r"^update$", views.update_cart, name='update'),
    url(r"^query$", views.query_cart, name='query'),
]