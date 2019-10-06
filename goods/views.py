from django.shortcuts import render
from django.http.response import HttpResponse
from django.core.paginator import Paginator
from . import models
# Create your views here.

def index(request):
    # return render(request, "goods/index.html")
    # 获取水果列表
    fruit_list = models.GoodInfo.objects.filter(gtype=1).filter(isDelete=False)
    fruit_order_new = fruit_list.order_by('-id')[:4]
    fruit_order_click = fruit_list.order_by('-click')[:3]
    # 判断当前是否登陆
    user_name = request.session.get('uname', default="")
    print(user_name)
    context = {
        "title": "首页",
        "user_name": user_name,
        "fruit_new": fruit_order_new,
        "fruit_click": fruit_order_click,
        "fruit_type": fruit_list[0].gtype
    }
    return render(request, "goods/index.html", context=context)


def detail(request):
    get_var = request.GET
    request_id = get_var['item']

    #获取数据
    detail_info = models.GoodInfo.objects.get(pk=request_id)
    # 获取同类型的最新3个数据
    same_type = detail_info.gtype
    new_object = models.GoodInfo.objects.filter(gtype=same_type).order_by('-id')[:3]


    context = {
        "title": detail_info.title,
        "object": detail_info,
        "same_type": new_object,
    }
    return render(request, "goods/detail.html", context=context)


def goods_list(request):
    # 获取类型
    re_type = request.GET['type']
    # 获取用户想要的页数
    re_page = request.GET['page']
    # 获取排序规则
    re_order = request.GET['order']
    object_all = models.GoodInfo.objects.filter(gtype=re_type)
    # 做排序
    if re_order == "1":
        object_all = object_all.order_by('id')
    elif re_order == "2":
        object_all = object_all.order_by('-price')
    else:
        object_all = object_all.order_by('-click')
    # 分页，1页10个对象
    page_object = Paginator(object_all, 10)

    revc_page = page_object.page(re_page)
    # 当前页码
    curr_page_num = revc_page.number
    # 获取上和下一页 页码
    if revc_page.has_previous() is True:
        pre_page = curr_page_num - 1
    else:
        pre_page = -1
    if revc_page.has_next() is True:
        next_page = curr_page_num + 1
    else:
        next_page = -1

    # 取全部页码数，仅返回前3页,如果超出，则额外显示多2页，始终显示第1第2页。
    page_range = page_object.page_range
    print("全部页码数：%s"%(page_range) )
    if len(page_range) - int(re_page) > 2:
        # 超出3页范围
        first_page = page_range[:1]
        second_page =  page_range[1:2]
        # 取前2页
        first_two_pages = page_range[int(re_page) - 3:int(re_page)-1]
        # 取后2页
        after_two_pages = page_range[int(re_page):int(re_page)+2]
        print("前2页%s" % (first_two_pages))
        print("后2页%s" % (after_two_pages))
        # 如果前2页取出来后，第1或第2页不包含在内，证明前面有跨越，应该给予用户提示
        # print(second_page[0] in first_two_pages)
        # 前2页取不出来，证明在1或2页中
        if len(first_two_pages) == 0:
            # print("判断11中")
            pages_list = first_page + second_page  + [curr_page_num] + after_two_pages
            pages = list(set(pages_list))
            # 按原先顺序排序
            pages.sort(key=pages_list.index)
            # print(pages)
        elif second_page[0] in first_two_pages or 3 in first_two_pages:
            # print("判断12中")
            # 此判断用于判断1和2页是否包含在内,另外如果前2页有第3页比较特殊，需要走这个判断
            pages_list = first_page + second_page + first_two_pages + [curr_page_num] + after_two_pages
            pages = list(set(pages_list))
            # 按原先顺序排序
            pages.sort(key=pages_list.index)
        else:
            # print("判断13中")
            # 如果不包含在内，在前面提示...
            pages_list = first_page + second_page + ["..."] + first_two_pages + [curr_page_num] + after_two_pages

            pages = list(set(pages_list))
            # 按原先顺序排序
            pages.sort(key=pages_list.index)
            # print(pages)
        more = True
    else:
        # print("判断2中")
        if int(re_page) == 3:
            pages = page_range
            if len(page_range) > 3:
                more = True
            else:
                more = False
        elif int(re_page) > 2:
            print("判断21中")
            # 没有超出3页范围，但是当前页不是第一页，证明在尾部几页
            first_page = page_range[:1]
            second_page = page_range[1:2]

            # 取前2页
            first_two_pages = page_range[int(re_page) - 3:int(re_page)-1]
            # 取余下页数
            after_two_pages = page_range[int(re_page):]
            print("前2页%s" % (first_two_pages))
            print("后2页%s" % (after_two_pages))
            # 和1，2页有跨越时，应当给予用户提示
            pages_list = first_page + second_page + ["..."] + first_two_pages + [curr_page_num] + after_two_pages
            pages = list(set(pages_list))
            # 按原先顺序排序
            pages.sort(key=pages_list.index)
            # print(pages)
            more = False
        else:
            print("判断22中")
            # 没有超出范围
            pages = page_range
            more = False

    # 新品推荐2个
    same_fruit = object_all.order_by('-id')[:2]
    context = {
        "title": models.TypeInfo.objects.get(pk=re_type),
        "num_page": page_object.num_pages,
        "curr_page_object": revc_page,
        "pre_page": pre_page,
        "next_page": next_page,
        "curr_page_num": curr_page_num,
        "page_range": pages,
        "curr_type": re_type,
        "curr_order": re_order,
        "pages_more": more,
        "same_fruit": same_fruit

    }
    #return HttpResponse(revc_page)
    return render(request, template_name='goods/list.html', context=context)