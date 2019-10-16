from django.shortcuts import render, redirect
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import UserInfo
from df_goods.models import GoodInfo
import sys

import hashlib


# Create your views here.
def judge_vaild(func):
    """
    :param func:
    :param request:
    :return:
    用于判断session是否过期，如果session过期，删除改session,并且跳转到登录页
    """
    def wrapper(request, *args, **kwargs):
        if request.session.get("uid") is None or request.session.get_expiry_age() <= 1:
            # 如果未登陆状态，或者会话过期执行此分支
            # 获取用户登陆前访问的网址，用于登陆后，返回
            # 获取用户登陆前的url
            full_path = request.get_full_path()
            # 如果直接登陆，则转到首页
            if full_path == "/user/login":
                full_path = "/"
            # 判断是否通过AJAX访问
            if request.is_ajax():
                json = JsonResponse({'redirect': '1', 'address': '/user/login'})
                json.set_cookie('url', full_path)
                return json
            else:
                red = HttpResponseRedirect("/user/login")
                red.set_cookie('url', full_path)
                return red
        else:
            # 更新会话
            request.session.modified = True
            return func(request, *args, **kwargs)
    return wrapper

def user_login(request):
    context = {
        "title": "登陆",
        "user_name": request.session.get('uname', default='')
    }
    return render(request, "df_user/login.html", context=context)

def register(request):
    context = {
        "title": "注册"
    }
    return render(request, "df_user/register.html", context=context)

@judge_vaild
def index(request):
    return redirect(to=user_center_info)

def register_handler(request):
    post = request.POST
    upasswd = post["pwd"]
    cpasswd = post["cpwd"]
    if upasswd!= cpasswd:
        return redirect(register)
    uname = post["user_name"]
    uemaill = post["email"]

    userinfo = UserInfo()
    userinfo.uemail = uemaill
    userinfo.uname = uname
    # 加密密码
    h1 = hashlib.sha1()
    h1.update(upasswd.encode("utf-8"))
    entry_pass = h1.hexdigest()
    userinfo.upasswd = entry_pass
    # 保存用户信息
    userinfo.save()
    return redirect("df_user:user_login")


def register_exist(request):
    post = request.GET
    username = post["user"]
    count = UserInfo.objects.filter(uname=username).count()
    json_res = {"count": count}
    return JsonResponse(json_res)


def login_handler(request):
    # 登陆后，开启session和客户端交login_hanlder交互
    post = request.POST
    # 取出用户名和密码
    try:
        username = post["username"]
        userpwd = post["pwd"]
    except Exception as e:
        return JsonResponse({"result": 2})
    # 取出用户对象
    uinfo = UserInfo.objects.filter(uname=username)
    if len(uinfo) == 0:
        return JsonResponse({"result": 2})
    uinfo = uinfo[0]
    response = {}

    # 匹配密码
    sha1 = hashlib.sha1()
    sha1.update(userpwd.encode("utf-8"))
    upwd = sha1.hexdigest()
    if uinfo.upasswd == upwd:
        # 验证成功
        # return JsonResponse({"result": "0",})
        # 提取用户ID和用户名建立会话
        request.session['uid'] = uinfo.id
        request.session['uname'] = uinfo.uname
        # 10分钟过期
        request.session.set_expiry(600)
        # 如果登陆成功，应该返回到用户登陆之前的页面，在处理时，已经保存在cookies中
        # 如果cookies中没有，那就跳转到首页
        user_url = request.COOKIES.get("url")
        if user_url is None:
            user_url = "/"
        print("用户从url：%s跳转"%(user_url))
        response = {"result": 0, "redirect": user_url}
    else:
        response = {"result": 1}

    # 是否记住密码？如果是，则写到用户cookie,如果否，则把cooies重置
    recv_data = JsonResponse(response)
    if post["checked"] == "true":
        recv_data.set_cookie("username", username)
    else:
        recv_data.set_cookie("username", username, expires=-1)

    #

    return recv_data

@judge_vaild
def user_center_info(request):
    # 取出用户对象
    user = UserInfo.objects.filter(id=request.session.get("uid"))
    # 取用户最近浏览的5个
    cookies_goods = request.COOKIES.get("recently")
    recently_goods = []
    if cookies_goods is not None:
        cookies_list = cookies_goods.split(",")
        for i in cookies_list:
            recently_goods.append(GoodInfo.objects.get(id=i))


    if len(user) == 1:
        context = {
            "title": "用户中心",
            "user_name": request.session.get('uname', default=""),
            "uname": user[0].uname,
            "email": user[0].uemail,
            "phoneCall": user[0].uphone,
            "this": "user_center_info",
            "recently": recently_goods
        }
        return render(request, "df_user/user_center_info.html", context=context)




@judge_vaild
def user_center_order(request):
    context = {
        "title": "用户中心",
        "this": "user_center_order",
        "user_name": request.session.get('uname', default=""),
    }
    return render(request, "df_user/user_center_order.html", context=context)


@judge_vaild
def user_center_site(request):
    user = UserInfo.objects.filter(id=request.session.get("uid"))
    context = {
        "title": "用户中心",
        "this": "user_center_site",
        "user_name": request.session.get('uname', default=""),
        "shou": user[0].ushou,
        "address": user[0].uaddress,
        "youbian": user[0].uyoubian,
        "phoneCall": user[0].uphone,
        "user_name": request.session.get('uname', default=""),
    }
    return render(request, "df_user/user_center_site.html", context=context)


@judge_vaild
def user_center_site_handler(request):
    userinfo = UserInfo.objects.get(id=request.session.get("uid"))
    post = request.POST
    shou = post["shou"]
    address = post["address"]
    youbian = post["youbian"]
    phoneCall = post["phoneCall"]
    userinfo.ushou = shou.encode("utf-8")
    userinfo.uaddress = address.encode("utf-8")
    userinfo.uphone = phoneCall.encode("utf-8")
    userinfo.uyoubian = youbian.encode("utf-8")
    userinfo.save()
    context = {
        "title": "用户中心",
        "this": "user_center_site",
        "shou": userinfo.ushou,
        "address": userinfo.uaddress,
        "youbian": userinfo.uyoubian,
        "phoneCall": userinfo.uphone,
    }

    return render(request, "df_user/user_center_site.html", context=context)

def logout(request):
    # 清除登陆信息，并返回到主页
    request.session.flush()
    return redirect("/")
