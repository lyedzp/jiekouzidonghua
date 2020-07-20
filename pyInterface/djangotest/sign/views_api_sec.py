from django.contrib import auth
import base64
from .models import Event
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

# 用户认证
def user_auth(request):
    get_http_auth = request.META.get('HTTP_AUTHORIZATION', b'')
    auth_user = get_http_auth.split()

    try:
        auth_parts = base64.b64decode(auth_user[1]).decode('utf-8').partition(':')
        print(auth_parts)
    except IndexError:
        return "null"

    userid, password = auth_parts[0], auth_parts[2]
    print('***************%s'%userid)
    print('***************%s' % password)
    # user = django_auth.authenticate(usename=username,password=password)
    # user = auth.authenticate(username=userid,password=password)
    user = auth.authenticate(username=userid,password=password)
    print(user)
    if user is not None:
        auth.login(request, user)
        return "success"

    else:
        return "fail"

# 发布会查询接口，增加用户认证
def get_event_list(request):
    auth_result = user_auth(request)
    if auth_result == "null":
        return JsonResponse({'status':10011,'message':'user auth null'})
    if auth_result == "fail":
        return JsonResponse({'status':10012,'message':'user auth fail'})
    eid = request.GET.get('eid', '')
    name = request.GET.get('name', '')
    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'message': '参数不能为空'})

    if eid != '':
        try:
            int(eid)
        except ValueError:
            return JsonResponse({"status": 10025, "message": "eid格式错误"})
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({"status": 10022, "message": "查询结果为空"})
        else:
            event['id'] = result.id
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({"status": 200, "message": "查询成功", "data": event})
    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for i in results:
                event = {}
                event['id'] = i.id
                event['name'] = i.name
                event['limit'] = i.limit
                event['status'] = i.status
                event['address'] = i.address
                event['start_time'] = i.start_time
                datas.append(event)
            return JsonResponse({"status": 200, "message": "查询成功", "data": datas})
        else:
            return JsonResponse({"status": 10022, "message": "查询结果为空"})


