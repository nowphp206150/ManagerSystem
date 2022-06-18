from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django import forms
from app01.models import Admin,UserInfo,PrettyNum,Order
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import ValidationError
import random

class orderForm(forms.Form):
    order_id=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','readonly':'readonly','value':(datetime.now().strftime('%Y%m%d%H%M%S')+str(random.randint(10,100)))}))
    goods=forms.CharField(error_messages={'required':'请输入靓号'},widget=forms.TextInput(attrs={'class':'form-control'}))
    price=forms.IntegerField(error_messages={'required':'请输入价格'},widget=forms.NumberInput(attrs={'class':'form-control'}))
    status=forms.IntegerField(widget=forms.Select(attrs={'class':'form-control'},choices=((0,'待支付'),(1,'已支付'))))
    user_id=forms.IntegerField(widget=forms.Select(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        # 执行父类构造方法
        super(orderForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].widget.choices=UserInfo.objects.all().values_list('id','name')

    def clean_order_id(self):
        order_id=self.cleaned_data['order_id']
        if Order.objects.filter(order_id=order_id):
            return order_id
        return datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(10, 100))

    def clean_goods(self):
        goods=self.cleaned_data['goods']
        if goods=='':
            raise ValidationError('请输入靓号')
        else:
            if PrettyNum.objects.filter(mobile=goods):
                return goods
            else:
                raise ValidationError('输入商品名错误')

    def clean_price(self):
        price=self.cleaned_data['price']
        if not price:
            raise ValidationError("请输入价格")
        return price

def order_list(request):
    '''
    展示所有订单
    :param request:
    :return:
    '''
    if not request.session.get('info'):
        return redirect('/login/')
    page=request.GET.get('page')
    form=orderForm(request.GET)
    orders=Order.objects.all()
    users=UserInfo.objects.all().values_list('id','name')
    orders=list(orders)
    num_user=dict()
    for user in users:
        num_user[user[0]]=user[1]
    for order in orders:
        order.user_id=num_user[order.user_id]
    div, duo = divmod(len(orders), 8)
    if duo:
        div = div + 1
    # 边缘条件判断
    if page == None:
        page = 1
    else:
        page = int(page)
        if page <= 0:
            page = 1
        elif page > div:
            page = div
    # 计算每一页的起始和结束的数据编号
    end = (page - 1) * 8 + 7
    start = end - 7
    # 判断最后一页
    end = min(end, len(orders))
    orders = orders[start:end + 1]
    # 判断现在这页前面和后面是否分别有五页
    ranges = [i for i in range(max(page - 5, 1), min(page + 5, div) + 1)]
    return render(request,'order_list.html',{'form':form,'orders':orders,'ranges': ranges, 'page': page})

@csrf_exempt
def order_add(request):
    '''
    添加订单
    :param request:
    :return:
    '''
    print(request.POST)
    form=orderForm(request.POST)
    if form.is_valid():
        '''有这条记录的话就修改，bug：由于公用一个模态框，保存只能触发一个ajax请求了'''
        order=Order.objects.filter(order_id=form.cleaned_data.get('order_id'))
        if order:
            order.update(**form.cleaned_data)
        else:
            order.create(**form.cleaned_data)
        return JsonResponse({'status':True})
    else:
        error = form.errors
        return JsonResponse({'status':False,'error':error})

def order_delete(request):
    '''
    删除zhi'di
    :param request:
    :return:
    '''
    order_id=request.GET.get('order_id')
    if Order.objects.filter(order_id=order_id).delete():
        return HttpResponse('删除成功')
    else:
        return HttpResponse('删除失败')

@csrf_exempt
def order_edit(request):
    '''
    编辑订单信息
    :param request:
    :return:
    '''
    if request.method=='GET':
        order_id=request.GET.get('order_id')
        order=Order.objects.filter(order_id=order_id).first()
        result=dict()
        if order:
            result={
                'status':True,
                'data':{
                    'order_id':order.order_id,
                    'goods':order.goods,
                    'price':order.price,
                    'status':order.status,
                    'user_id':order.user_id
                }
            }
        else:
            result={
                'status':False
            }
        return JsonResponse(result)
    else:
        pass
