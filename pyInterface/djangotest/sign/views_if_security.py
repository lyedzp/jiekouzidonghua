#encoding=utf-8
import time,hashlib
from django.http import JsonResponse
from .models import Event
from django.core.exceptions import ValidationError
# 用户签名+时间戳
def user_sign(request):
    if request.method=="POST":
        client_time=request.POST.get('time','')#客户端时间戳
        client_sign=request.POST.get('sign','')#客户端签名
    else:
        return 'error'
    if client_time=='' or client_sign=='':
        return 'sign null'
    #服务器时间
    now_time=time.time()
    server_time=str(now_time).split('.')[0]
    print("server-time:"+server_time)
    #获取时间差
    time_difference=int(server_time)-int(client_time)
    if time_difference >= 60:
        return 'timeout'

    #签名检查
    md5=hashlib.md5()
    sign_str=client_time+"&Guest-Bugmaster"
    sign_bytes_utf8=sign_str.encode(encoding="utf-8")
    md5.update(sign_bytes_utf8)
    server_sign = md5.hexdigest()

    if server_sign!=client_sign:
        return "sign fail"
    else:
        return "sign success"

#添加发布会接口，增加签名+时间戳
def add_event(request):
    sign_result=user_sign(request)
    if sign_result=="error":
        return JsonResponse({'status':10011,'message':'request error'})
    elif sign_result=="sign null":
        return JsonResponse({'status':10012,'message':'user sign null'})
    elif sign_result=="timeout":
        return JsonResponse({'status':10013,'message':"user sign timeout"})
    elif sign_result=="sign fail":
        return JsonResponse({'status':10014,'message':'user sign error'})
    else:
        eid = request.POST.get('eid', '')  # 发布会id
        name = request.POST.get('name', '')  # 发布会名称
        limit = request.POST.get('limit', '')  # 发布会限制人数
        status = request.POST.get('status', '')  # 发布会状态
        address = request.POST.get('address', '')  # 发布会地址
        start_time = request.POST.get('start_time', '')  # 发布会开始时间
        if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
            # 返回json格式，别人才好解析
            return JsonResponse({"status": 10021, "message": "必传参数为空"})
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
            Event.objects.create(id=eid, name=name, limit=limit, status=status, address=address, start_time=start_time)
        except ValidationError:
            error = '发布会时间格式错误，It must be YYYY-MM-DD HH:MM:SS'
            return JsonResponse({'status': 10024, 'message': error})
        return JsonResponse({'status': 200, 'message': '发布会新增成功'})