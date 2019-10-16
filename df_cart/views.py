from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from .models import CartInfo
from df_user.views import judge_vaild
from df_user.models import UserInfo
from df_goods.models import GoodInfo
from django.http.response import HttpResponse

# Create your views here.

@judge_vaild
def index(request):
    # 取用户商品
    user_cart =  CartInfo.objects.filter(user=request.session["uid"])
    context = {
        "title": "购物车",
        "objects": user_cart,
        "cart_count": len(user_cart),
        "user_name": request.session["uname"]
    }

    return render(request, template_name="df_cart/cart.html", context=context)


@judge_vaild
def add_to_cart(request):
    # 商品ID
    goods_id = request.GET["id"]
    goods_count = request.GET["count"]
    goods_object = CartInfo()
    # 取出相应对象
    user = UserInfo.objects.get(pk=request.session['uid'])
    goods = GoodInfo.objects.get(pk=goods_id)
    # 保存商品到购物车，如果是新数据，则新增
    exist_goods_object = CartInfo.objects.filter(user=request.session['uid']).filter(goods=goods_id)
    # print(len(exist_goods_object))
    # 大于等于1则已存在相应商品，则修改数量即可
    save_result = "true"
    if len(exist_goods_object) >= 1:
        exist_goods_object[0].count += int(goods_count)
        try:
            exist_goods_object[0].save()
        except Exception as e:
            save_result = "fail"
    else:
        goods_object.user = user
        goods_object.count = goods_count
        goods_object.goods = goods
        # 保存数据，如果是新商品，
        try:
            goods_object.save()
        except Exception as e:
            save_result = "fail"

        # 获取用户购物车商品数量
    cart_count = CartInfo.objects.filter(user=request.session['uid']).count()

    if request.is_ajax():
        return JsonResponse({"result": save_result, "cart_count": cart_count})
    else:
        return redirect(to='/cart')

@judge_vaild
def del_from_cart(request):
    cart_id = request.GET["id"]
    try:
        object = CartInfo.objects.get(pk=cart_id)
        object.delete()
    except Exception as e:
        pass

    json = JsonResponse({"result": "ok"})
    return json

@judge_vaild
def update_cart(request):
    cart_id = request.GET["id"]
    goods_count = request.GET["count"]
    try:
        object = CartInfo.objects.get(pk=cart_id)
        object.count = int(goods_count)
        object.save()
        json = JsonResponse({"result": object.count})
    except Exception as e:
        # 失败返回原先的数量
        json = JsonResponse({"result": goods_count})

    print(json)
    return json

@judge_vaild
def query_cart(request):
    # 查询购物车商品数量
    object = CartInfo.objects.filter(user=request.session['uid'])

    return JsonResponse({"cart_count": len(object)})
