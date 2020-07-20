from django.contrib import admin
from sign.models import Event,Guest

# Register your models here.
# django�Դ��ĺ�̨�������ݿ�ӳ�䣬��Ҫ���ǰ�models�ﴴ���ı�ӳ�䵽��̨����
# ��Ϊ�����б����ֶη�ʽ��ʾ���������Զ���ʽ��ʾ
class EventAdmin(admin.ModelAdmin):
    list_display = ['name','limit','status','address','start_time','create_time']
    search_fields = ['name']#������������������name
    list_filter = ['status']#������������������status

class GuestAdmin(admin.ModelAdmin):
    list_display = ['event','realname','phone','email','sign','create_time']
# ��Event��ע�ᵽ��̨
admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)