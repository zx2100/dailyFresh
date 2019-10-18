from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r"^$", views.index),
    url(r"^register$", views.register),
    url(r"^register_handler$", views.register_handler),
    url(r"^login$", views.user_login, name="user_login"),
    url(r"^register_exist$", views.register_exist),
    url(r"^login_handler$", views.login_handler),
    url(r"^user_center_info$", views.user_center_info),
    url(r"^user_center_order$", views.user_center_order),
    url(r"^user_center_site$", views.user_center_site),
    url(r"^user_center_site_handler$", views.user_center_site_handler),
    url(r'^logout', views.logout),
    url(r'^get_name', views.get_uname),

]
