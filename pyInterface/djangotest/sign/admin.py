from django.contrib import admin
from sign.models import Event,Guest

# Register your models here.
# django自带的后台，做数据库映射，主要就是把models里创建的表映射到后台管理
# 是为了让列表以字段方式显示，而不是以对象方式显示
class EventAdmin(admin.ModelAdmin):
    list_display = ['name','limit','status','address','start_time','create_time']
    search_fields = ['name']#搜索栏，搜索条件是name
    list_filter = ['status']#过滤器，过滤条件是status

class GuestAdmin(admin.ModelAdmin):
    list_display = ['event','realname','phone','email','sign','create_time']
# 把Event表注册到后台
admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)