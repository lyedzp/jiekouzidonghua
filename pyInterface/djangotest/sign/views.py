from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
# 导入django认证模块
from django.contrib import auth

# 导入该模块后，用户必须进行登录才能访问登录后的页面
from django.contrib.auth.decorators import login_required
# Create your views here
from sign.models import Event,Guest
#分页模块,EmptyPage,PageNotAnInteger是处理异常的
from  django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# 首页
def index(request):
    return render(request,'index.html')

# 登录处理
def login_action(request):
    if request.method == "POST":
        login_username = request.POST.get('uname')
        login_password = request.POST.get('pwd')
        if login_username == ''or login_password == '':
            return render(request, 'index.html',{'error':'username or password is null'})
        else:
            # 这行代码会去数据库查用该账号和密码登录的用户名是否存在
            user = auth.authenticate(username = login_username,password = login_password)
            # 不为none说明用户在数据库存在
            if user is not None:
                auth.login(request,user)#验证登录
                # 登录成功后跳转
                response = HttpResponseRedirect('/event_manage/')
                # 将登录用户名放入浏览器cookie,失效时间为10秒
                # response.set_cookie('user',login_username,10)
                # 存session
                request.session['user'] = login_username
                return response
            else:
                return render(request, 'index.html', {'error': 'username or password is not right'})


    else:
        return render(request, 'index.html')
# 发布会管理
@login_required()
def event_manage(request):
    # 获取浏览器的cookie
    # user = request.COOKIES.get('user')
    # 获取浏览器session
    user = request.session.get('user')
    events = Event.objects.all()
    for event in events:
        print(event.name)
        print(event.address)
    return render(request,'event_manage.html',{'user':user,"event":events})
# 退出系统
@login_required()
def logout(request):
    auth.logout(request)#退出登录，这个退出登录会清除cookie
    response = HttpResponseRedirect('/index/')
    return response

# 发布会管理系统名称搜索
@login_required()
def search_name(request):
    user = request.session.get('user')
    search_name = request.GET.get('name')
    print(search_name)
    # name__contains，加了__contains代表模糊查询
    events = Event.objects.filter(name__contains=search_name)
    return render(request, 'event_manage.html', {'user':user,"event": events})

# 嘉宾管理页手机号搜索搜索
@login_required()
def search_phone(request):
    user = request.session.get('user')
    search_phone = request.GET.get('phone','')
    #加了__contains代表模糊查询
    guests = Guest.objects.filter(phone__contains=search_phone)
    if len(guests)==0:
        return render(request, 'guest_manage.html', {'user': user, "hint": "暂无搜索内容"})
    paginator = Paginator(guests, 2)
    # 获取前端传来的页码
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整数，取第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {'user':user,"guest": contacts})

# 嘉宾管理
@login_required()
def guest_manage(request):
    user = request.session.get('user')
    guests = Guest.objects.all()
    # # 查出嘉宾表所有数据且每页显示2条数据
    # page = Paginator(guests,2)
    # # page.count,嘉宾表总数据条数,page.page_range分了几页
    # print(page.count)
    # print(page.page_range)
    # page1 = page.page(1)
    # # 第一页有哪些数据
    # print(page1.object_list)
    # page2 = page.page(2)
    # #第二页是从第几条数据开始，第几条数据结束
    # print(page2.start_index())
    # print(page2.end_index())
    # #第二页的上一页页码
    # print(page2.previous_page_number())
    # #是否有上一页
    # print(page2.has_previous())
    # # 是否有下一页
    # print(page2.has_next())
    paginator = Paginator(guests,2)
    # 获取前端传来的页码
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整数，取第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {'user': user, "guest": contacts})

#嘉宾签到页
def sign_index(request,event_id):
    # 通过id去Event表查数据，数据不存在就返回404
    event = get_object_or_404(Event,id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)#签到人数
    sign_list = Guest.objects.filter(event_id=event_id,sign=1)#已签到人数
    return render(request,'sign_index.html',{"event":event,"guest":guest_list.count(),"sign":sign_list.count()})

# 嘉宾签到处理
def sign_index_action(request,event_id):
    # 通过id去Event表查数据，数据不存在就返回404
    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)  # 签到人数
    sign_list = Guest.objects.filter(event_id=event_id, sign=1)  # 已签到人数
    sign_data = len(sign_list)
    phone = request.POST.get("phone")
    result = Guest.objects.filter(phone = phone)
    # 验证手机号码是否存在
    if not result:
        return render(request,'sign_index.html',{"event":event,"hint":"phone is not exist"
                                                 ,"guest":guest_list.count(),"sign":sign_list.count()})
    #验证手机号和发布会是否匹配
    result = Guest.objects.filter(phone=phone,event_id=event_id)
    if not result:
        return render(request, 'sign_index.html', {"event": event, "hint": "phone or event is wrong"
            , "guest": guest_list.count(), "sign": sign_list.count()})
    result = Guest.objects.filter(sign=0,phone=phone)
    if not result:
        return render(request, 'sign_index.html', {"event": event, "hint": "该用户已签到"
            , "guest": guest_list.count(), "sign": sign_list.count()})
    else:
        Guest.objects.filter(phone=phone,event_id=event_id).update(sign='1')
        return render(request, 'sign_index.html', {"event": event, "hint": "签到成功"
            , "guest": guest_list.count(), "sign": str(int(sign_data)+1),'sign_user':result})








