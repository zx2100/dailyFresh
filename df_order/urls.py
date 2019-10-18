from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r"^place$", views.place),
    url(r"^order_handler$", views.order_handler),
    url(r"^test$", views.test),
]