from django.db import models

# Create your models here.
# 创建和管理数据库

# 发布会签到系统
# 发布会管理表：--》创建发布会：id,名称，发布会时间，地点，场地人数，创建时间，状态
#嘉宾表：--》id,嘉宾类型（媒体，米粉，厂商），姓名，手机号，参加的哪场发布会，签到状态，创建时间

# 编程语言-->orm--》数据库驱动(pymysql)-->数据库，orm就是用编程语言的语法来操作数据库，而不是sql语句
# User表对象去查email = 2560547068@qq.com这条数据
# user1 = User.objects.get('email'='2560547068@qq.com')
# # 获取id值
# userl.id
# 获取密码值
# user1.password

# 通过orm来创建上面两张表,Event就是一张表（发布会管理表）
class Event(models.Model):
    name = models.CharField(max_length=100)#发布会名字
    limit = models.IntegerField()#限制人数
    status = models.BooleanField()#发布会状态
    address = models.CharField(max_length=400)#发布会地址
    start_time = models.DateTimeField()#发布会开始时间
    create_time = models.DateTimeField(auto_now=True)#自动获取当前时间

    def __str__(self):
        return self.name

# 嘉宾表
class Guest(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)#关联发布会
    realname = models.CharField(max_length=20)#姓名
    phone = models.CharField(max_length=16)#手机号
    email = models.CharField(max_length=100)#邮箱
    sign = models.BooleanField()#签到状态
    create_time = models.DateTimeField(auto_now=True)#创建时间
    class Meta:
        unique_together = ('phone','event')#嘉宾表里的联合主键是phone+event
    def __str__(self):
        return self.realname

