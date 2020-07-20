#encoding=utf-8
from django.test import TestCase
from .views import index
from django.contrib.auth.models import User
from .models import Event,Guest

# Create your tests here.
# 做django单元测试de
# class ViewTest(TestCase):
#     def test_index(self):
#         response = self.client.get('/index/')
#         # 断言响应的状态码是不是200
#         self.assertEqual(response.status_code,200)
#         # 断言response返回的页面是不是index.html页面
#         self.assertTemplateUsed(response,'index.html')

# class LoginActionTest(TestCase):
#     def setUp(self):
#         User.objects.create_user('admin','admin@123','admin123456')
#         user = User.objects.get(username = 'admin')
#         print(user.email)
#         print(user.password)
#     def tearDown(self):
#         pass
#     def test_login_action_success(self):
#         # 注意：django进行单元测试时，用的是测试环境数据库，里面没数据，所以测试登录要在初始化数据时往测试环境
#         #添加用户，并用该用户账号测试登录
#         user_info = {'uname':'admin','pwd':'admin123456'}
#         response = self.client.post('/login_action/',data=user_info)
#         self.assertEqual(response.status_code,302)
#
#     def test_login_action_username_password_null(self):
#         # 测试登录名或者密码为空
#         user_info = {'uname':'','pwd':''}
#         response = self.client.post('/login_action/',data=user_info)
#         self.assertIn(b'username or password is null',response.content)


# class EventActionTest(TestCase):
#     def setUp(self):
#         User.objects.create_user('admin', 'admin@123', 'admin123456')
#         Event.objects.create(name='xiaomi5',limit=2000,status=True,address='SC',start_time ='2018-09-09 11:20:00',
#                              create_time='2018-09-09 11:20:00')
#         data = {'uname':'admin','pwd':'admin123456'}
#         # 测发布会管理，要先登录
#         self.client.post('/login_action/',data=data)
#
#     def test_event_manage_success(self):
#         response = self.client.post('/event_manage/')
#         print(response.content)
#         self.assertEqual(response.status_code,200)
#         self.assertIn(b'xiaomi5',response.content)
#         self.assertIn(b'SC', response.content)
#
#     def test_search_name(self):
#         # 测试发布会搜索
#         response = self.client.get('/search_name/',{'name':'xiaomi5'})
#         self.assertEqual(response.status_code,200)
#         self.assertIn(b'xiaomi5',response.content)

class GuestActionTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@123', 'admin123456')
        Event.objects.create(name='xiaomi5',limit=2000,status=True,address='SC',start_time ='2018-09-09 11:20:00',
                                     create_time='2018-09-09 11:20:00')
        Guest.objects.create(realname='liangyuee',phone='19380978898',email='234@qq.com',sign=False,create_time='2018-09-09 11:20:00',event_id=1)
        data = {'uname':'admin','pwd':'admin123456'}
        self.client.post('/login_action/',data=data)
    #     测试签到成功
    def test_sign_index_action_success(self):
        response = self.client.post('/sign_index_action/1/',{'phone':'19380978898'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'sign success',response.content)



