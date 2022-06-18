from django.db import models

# Create your models here.

class Department(models.Model):
    title=models.CharField(max_length=32)

class UserInfo(models.Model):
    name=models.CharField(max_length=16)
    password=models.CharField(max_length=64)
    age=models.CharField(max_length=20)
    account=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    create_time=models.DateField(verbose_name="入职时间")
    sex=models.SmallIntegerField(null=True,blank=True)
    depart=models.ForeignKey(to="Department",to_field="id",on_delete=models.CASCADE)
    ip=models.CharField(max_length=255)

class PrettyNum(models.Model):
    mobile=models.CharField(verbose_name='手机号',max_length=15,primary_key=True)
    price=models.IntegerField(verbose_name='价格',default=0)
    level=models.SmallIntegerField(verbose_name='级别',default=1)
    status=models.SmallIntegerField(verbose_name='状态',default=0)

class Admin(models.Model):
    name=models.CharField(verbose_name='管理员姓名',max_length=32,primary_key=True)
    password=models.CharField(max_length=32)

class Order(models.Model):
    order_id=models.CharField(verbose_name='订单号',max_length=32)
    goods=models.CharField(verbose_name='商品名',max_length=32)
    price=models.IntegerField(verbose_name='价格')
    status=models.SmallIntegerField(verbose_name='状态')
    user_id=models.BigIntegerField(verbose_name='用户id')