from django.shortcuts import render
from django.http.response import HttpResponse
from df_cart.models import CartInfo
from df_user.models import UserInfo
from df_user.views import judge_vaild
from .models import OrderInfo, OrderDetailInfo
import hashlib

from django.http.response import JsonResponse
from django.db import transaction

# Create your views here.
@judge_vaild
def place(request):
    carts_id = request.GET.getlist("cart_id")
    carts_objects = []
    total = 0
    for i in carts_id:
        # 取出购物车对象
        cart = CartInfo.objects.get(pk=i)
        # 计算小计金钱
        subtotal = cart.goods.price * cart.count
        # 计算合计
        total += subtotal
        # 构建新对象返回
        o_cart = {
            "subtotal": subtotal,
            "object": cart
        }
        carts_objects.append(o_cart)

    # 获取收获人信息
    user = UserInfo.objects.get(pk=request.session['uid'])
    # 邮费
    postage = 10
    # 总金额大于100元包邮
    if total > 100:
        postage = 0

    payment = total + postage
    context = {
        "title": "确认订单",
        "carts": carts_objects,
        "user": user,
        "total": total,
        "count": len(carts_objects),
        "postage": postage,
        "payment": payment,
    }

    return render(request, template_name="df_order/order_place.html", context=context)


@transaction.atomic
def order_handler(request):

    carts_id = request.POST.get('cartid')
    if carts_id is None:
        raise RuntimeError("carts info error")

    # 分割购物车ID
    carts_list = carts_id.split("&")
    carts_object_list = []
    # 小计合计
    total = 0
    # 邮费
    postage = 0
    # 应付款
    payment = 0

    # 循环取出对象，并且判断库存
    for i in carts_list:
        carts_object = CartInfo.objects.get(pk=i)

        # 首先，先减少库存
        try:
            # 减少库存
            carts_object.goods.inventory = carts_object.goods.inventory - carts_object.count
            carts_object.goods.save()
        except Exception as e:
            pass

        # 计算小计
        subtotals = int(carts_object.count) * carts_object.goods.price
        # 计算总价
        total += subtotals
        order_item = {
            "subtotal": subtotals,
            "item": carts_object
        }
        carts_object_list.append(order_item)
        # 随后删除购物车对象
        carts_object.delete()

    # 邮费,总金额小于100，收取邮费10元
    if total < 100:
        postage = 10

    payment = total + postage
    # 写订单信息
    order_info = OrderInfo()
    # 应付总额
    order_info.payment = payment
    order_info.phone = carts_object_list[0]["item"].user.uphone
    order_info.address = carts_object_list[0]["item"].user.uaddress

    # 收货地址
    order_info.consignee = carts_object_list[0]["item"].user.ushou
    # 订单归属
    order_info.user = carts_object_list[0]["item"].user
    order_info.status = "未付款"
    order_info.payment_status = False
    # 保存，生成订单，然后生成订单号，并写入,先初始化为0
    order_info.another_id = 0
    order_info.save()
    # 重新写入订单编号
    order_id = Order_serialize(request.session['uid'], order_info.pk)()
    order_info.another_id = order_id
    # 重新保存
    order_info.save()

    # 开始写商品详情,以下循环把购物车的商品添加进去
    # OrderInfo,主要保存收件人信息，地址，联系方式，是否付款（默认false）
    try:
        for order in carts_object_list:
            order_detail_info = OrderDetailInfo()
            order_detail_info.order = order_info
            order_detail_info.goods = order['item'].goods
            order_detail_info.count = order['item'].count
            order_detail_info.price = order['item'].goods.price
            order_detail_info.subtotal = order['subtotal']
            order_detail_info.pic = order['item'].goods.pic
            order_detail_info.title = order['item'].goods.title
            order_detail_info.unit = order['item'].goods.unit
            # 属于那个订单
            order_detail_info.order_aff = order_info.another_id
            print(order_detail_info.order_aff)
            order_detail_info.save()
            print("xx")
    except Exception as e:
        print(e)
        raise RuntimeError(e)
    return JsonResponse({"result": "ok"})




class Order_serialize(object):
    def __init__(self, uid, order_id):
        self.uid = uid
        self.order_id = order_id

    def test(self):
        # 生成订单号
        # 规则: 用户ID+订单ID+时间戳取余
        result = ""
        uid = self.uid
        order_id = self.order_id

        # 日期序列取余数，即0-9999随机
        import time
        re_time = int(time.time()) % 9999
        result = ("%s%s%s" % (uid, order_id, re_time))
        return result

    def __call__(self, *args, **kwargs):
        return self.test()


def test(request):
    result = Order_serialize("1", "433")
    return HttpResponse(int(result()))