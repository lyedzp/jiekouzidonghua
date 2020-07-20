from django.urls import path
from sign import views_api,views_api_sec,views_if_security
urlpatterns = [
    path('add_event/', views_api.add_event,name='add_event'),
    path('get_event_list/', views_api.get_event_list,name='get_event_list'),
    path('user_sign/', views_api.user_sign,name='user_sign'),
    path('add_guest/', views_api.add_guest,name='add_guest'),
    path('sec_get_event_list/', views_api_sec.get_event_list,name='get_event_list'),
    path('sec_add_event/', views_if_security.add_event,name='add_event'),
]
