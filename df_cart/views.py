from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.


def index(request):
    context = {
        "title": "购物车"
    }

    return render(request, template_name="df_cart/cart.html", context=context)