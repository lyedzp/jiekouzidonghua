#encoding=utf-8
from .models import Event,Guest
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.exceptions import ValidationError,ObjectDoesNotExist
import time
# 添加发布会接口
def add_event(request):
    if request.method=="POST":
        eid = request.POST.get('eid','')#发布会id
        name = request.POST.get('name','')#发布会名称
        limit = request.POST.get('limit','')  # 发布会限制人数
        status = request.POST.get('status','')  # 发布会状态
        address = request.POST.get('address','')  # 发布会地址
        start_time = request.POST.get('start_time','')  # 发布会开始时间
        if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
            # 返回json格式，别人才好解析
            return JsonResponse({"status":10021,"message":"必传参数为空"})
        try:
            int(eid)
        except ValueError:
            return JsonResponse({"status": 10025, "message": "eid格式错误"})
        result = Event.objects.filter(id=eid)
        if result:
            return JsonResponse({"status": 10022, "message": "发布会id已存在"})
        result = Event.objects.filter(name=name)
        if result:
            return JsonResponse({"status": 10023, "message": "发布会名称重复"})
        if status == '':
            status = 1
        try:
            Event.objects.create(id=eid,name=name,limit=limit,status=status,address=address,start_time=start_time)
        except ValidationError:
            error = '发布会时间格式错误，It must be YYYY-MM-DD HH:MM:SS'
            return JsonResponse({'status':10024,'message':error})
        return JsonResponse({'status':200,'message':'发布会新增成功'})
    else:
        return JsonResponse({"status": 10031, "message": "请求方法错误"})

# 发布会查询
def get_event_list(request):
    eid = request.GET.get('eid','')
    name = request.GET.get('name','')
    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'message': '参数不能为空'})


    if eid!='':
        try:
            int(eid)
        except ValueError:
            return JsonResponse({"status": 10025, "message": "eid格式错误"})
        event={}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({"status": 10022, "message": "查询结果为空"})
        else:
            event['id']=result.id
            event['name']=result.name
            event['limit']=result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({"status": 200, "message": "查询成功","data":event})
    if name!='':
        datas=[]
        results = Event.objects.filter(name__contains=name)
        if results:
            for i in results:
                event = {}
                event['id']=i.id
                event['name'] = i.name
                event['limit'] = i.limit
                event['status'] = i.status
                event['address'] = i.address
                event['start_time'] = i.start_time
                datas.append(event)
            return JsonResponse({"status": 200, "message": "查询成功","data":datas})
        else:
            return JsonResponse({"status": 10022, "message": "查询结果为空"})


# 用户签到接口
def user_sign(request):
    eid = request.POST.get('eid','')#发布会签到id
    phone = request.POST.get('phone','')#手机号
    if eid=='' or phone=='':
        return JsonResponse({'status': 10021, 'message': '参数不能为空'})
    try:
        int(eid)
    except ValueError:
        return JsonResponse({"status": 10028, "message": "eid格式错误"})
    try:
        int(phone)
    except ValueError:
        return JsonResponse({"status": 10029, "message": "phone格式错误"})
    result = Event.objects.filter(id = eid)
    # 如果发布会不存在
    if not result:
        return JsonResponse({"status": 10022, "message": "发布会不存在"})
    # 发布会为关闭状态
    result = Event.objects.get(id = eid).status
    if not result:
        return JsonResponse({"status": 10023, "message": "发布会为关闭状态，不能签到"})

    #对时间的处理
    event_time=Event.objects.get(id=eid).start_time
    timeArray=time.strptime(str(event_time),'%Y-%m-%d %H:%M:%S')
    # 转化成时间戳，如1573329290，只有转化成为int的时间戳，才能比较
    e_time=int(time.mktime(timeArray))

   #取当前时间
    now_time = str(time.time())
    ntime=now_time.split('.')[0]
    n_time = int(ntime)
    if n_time>e_time:
        return JsonResponse({"status": 10024, "message": "发布会已开始或已结束"})

    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({"status": 10025, "message": "手机号为空"})
   #用户签到手机号与发布会不对应
    result=Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return JsonResponse({"status": 10026, "message": "此手机号没有参加该发布会"})
    #用户是否已经签过到
    result = Guest.objects.get(phone=phone, event_id=eid).sign
    if result:
        return JsonResponse({"status": 10027, "message": "此手机号已经签到"})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign=1)
        return JsonResponse({"status": 200, "message": "签到成功"})

#嘉宾添加接口
def add_guest(request):
    if request.method=="POST":
        relname = request.POST.get('relname', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        sign = request.POST.get('sign', '')
        event_id = request.POST.get('event_id', '')
        if relname == '' or phone == '' or email == '' or event_id == '':
            return JsonResponse({'status': 10021, 'message': '参数不能为空'})
        result = Event.objects.filter(id=event_id)
        if not result:
            return JsonResponse({'status': 10022, 'message': '发布会不存在'})
        result = Event.objects.get(id=event_id).status
        if not result:
            return JsonResponse({'status': 10023, 'message': '发布会状态不可用'})

        if sign=='':
            sign=0

        result=Event.objects.get(id=event_id).limit#发布会限制人数
        count=Guest.objects.filter(event_id=event_id)#已参加该发布会的人数
        if len(count)>=result:
            return JsonResponse({'status': 10024, 'message': '发布会已满员'})

            # 对时间的处理
        event_time = Event.objects.get(id=event_id).start_time
        timeArray = time.strptime(str(event_time), '%Y-%m-%d %H:%M:%S')
        # 转化成时间戳，如1573329290，只有转化成为int的时间戳，才能比较
        e_time = int(time.mktime(timeArray))

        # 取当前时间
        now_time = str(time.time())
        ntime = now_time.split('.')[0]
        n_time = int(ntime)

        if n_time>e_time:
            return JsonResponse({'status': 10025, 'message': '发布会已经开始，不可参加'})
        # Guest.objects.create(id=gid, realname=relname, phone=int(phone), email=email, event_id=int(event_id), sign=sign)
        try:
            Guest.objects.create(realname=relname,phone=int(phone),email=email,event_id=int(event_id),sign=sign)
        except ValueError:
            return JsonResponse({'status': 10026, 'message': '手机号码已存在'})
        return JsonResponse({'status': 200, 'message': '嘉宾添加成功'})
