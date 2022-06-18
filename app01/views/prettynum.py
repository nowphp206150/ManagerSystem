from django.core.validators import RegexValidator
from django.forms import ValidationError
from django.shortcuts import render,redirect
from app01.models import PrettyNum
from django import forms

def prettynum_list(request):
    '''
    靓号展示
    :param request:
    :return:
    '''
    query=request.GET.get('query')
    page=request.GET.get('page')
    nums=None
    if query:
        nums=PrettyNum.objects.filter(mobile__contains=query).order_by('-level','status')
    else:
        query=''
        nums=PrettyNum.objects.all().order_by('-level','status')
    # 每页显示8条，该函数是除法函数，第一个是商第二个是余数，最后得到最终的页数
    div,duo=divmod(nums.count(),8)
    if duo:
        div=div+1
    # 边缘条件判断
    if page==None:
        page=1
    else:
        page=int(page)
        if page<=0:
            page=1
        elif page>div:
            page=div
    # 计算每一页的起始和结束的数据编号
    end=(page-1)*8+7
    start=end-7
    # 判断最后一页
    end=min(end,nums.count())
    nums=nums[start:end+1]
    # 判断现在这页前面和后面是否分别有五页
    ranges=[i for i in range(max(page-5,1),min(page+5,div)+1)]
    return render(request,'prettynum_list.html',{'nums':nums,'query':query,'ranges':ranges,'page':page})

class PrettyForm(forms.Form):
    mobile=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True,validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误')],)
    price=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}),required=True)
    level=forms.IntegerField(widget=forms.Select(attrs={'class':'form-control'},choices=((1,'1级'),(2,'2级'),(3,'3级'),(4,'4级'),)),initial=1)
    status=forms.IntegerField(widget=forms.Select(attrs={'class':'form-control'},choices=((0,'未使用'),(1,'已占用'),)),initial=0)
    create_time=forms.DateTimeField(widget=forms.DateInput)

    def clean_mobile(self):
        mobile=self.cleaned_data['mobile']
        if PrettyNum.objects.filter(mobile=mobile):
            raise ValidationError("靓号已存在")
        return mobile

def prettynum_add(request):
    '''
    添加靓号
    :param request:
    :return:
    '''
    if request.method=='GET':
        form = PrettyForm()
        return render(request,'prettynum_add.html',{'form':form})
    else:
        form = PrettyForm(request.POST)
        if form.is_valid():
            data=form.data
            PrettyNum.objects.create(mobile=data.get('mobile'),price=data.get('price'),level=data.get('level'),status=data.get('status'))
            return redirect('/prettynum/')
        else:
            return render(request,'prettynum_add.html',{'form':form,'error':form.errors})

class PrettyEditForm(forms.Form):
    mobile=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True,validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误')],)
    price=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}),required=True)
    level=forms.IntegerField(widget=forms.Select(attrs={'class':'form-control'},choices=((1,'1级'),(2,'2级'),(3,'3级'),(4,'4级'),)),initial=1)
    status=forms.IntegerField(widget=forms.Select(attrs={'class':'form-control'},choices=((0,'未使用'),(1,'已占用'),)),initial=0)

def prettynum_edit(request):
    '''
    编辑靓号
    :param request:
    :return:
    '''
    if request.method=='GET':
        mobile=request.GET.get('mobile')
        forms=PrettyNum.objects.filter(mobile=mobile).first()
        forms={'mobile':forms.mobile,'price':forms.price,'level':forms.level,'status':forms.status}
        form = PrettyEditForm(forms)
        return render(request,'prettynum_edit.html',{'form':form})
    else:
        form=PrettyEditForm(request.POST)
        if form.is_valid():
            data=form.data
            PrettyNum.objects.filter(mobile=data.get('mobile')).update(price=data.get('price'),level=data.get('level'),status=data.get('status'))
            return redirect('/prettynum/')
        else:
            return render(request,'prettynum_edit.html',{'form':form,'error':form.errors})

def prettynum_delete(request):
    '''
    删除靓号
    :param request:
    :return:
    '''
    PrettyNum.objects.filter(mobile=request.GET.get('mobile')).delete()
    return redirect('/prettynum/')