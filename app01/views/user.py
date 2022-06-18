from django.shortcuts import render,redirect,HttpResponse
from app01.models import UserInfo,Department
from app01.views.md5 import md5

def index(request):
    # return render(request,"index_page.html",{"a":a})

    return render(request,'index_page.html')

def register(request):   #注册的页面
    if request.method=='GET':   # 进入登陆页面是get没有携带参数,注意必须是大写的get
        # print(type(request.GET.get("account")))
        return render(request,'register_page.html')
    else:     # post请求携带了用户名密码这些数据
        #  print(request.POST) 如果是post请求，这样获取数据
        username=request.POST.get('user')
        password=request.POST.get('pwd')
        age=request.POST.get('age')
        huawei={1:2,'huawei':2}
        print(type.objects.filter(type=1)[0].name)
        print(type.objects.filter())
        UserInfo.objects.create(name=username,password=password,age=age,ip=123456)
        return HttpResponse('注册成功')

def user_list(request):
    '''
    用户展示
    :param request:
    :return:
    '''
    if not request.session.get('info'):
        return redirect('/login/')
    page=request.GET.get('page')
    users = UserInfo.objects.all()
    users=list(users)
    for user in users:
        '''获得部门数字对应的部门名字'''
        user.depart_id=Department.objects.filter(id=int(user.depart_id)).first().title
        user.create_time=user.create_time.strftime('%Y-%m-%d')
    div,duo=divmod(len(users),8)
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
    end=min(end,len(users))
    users=users[start:end+1]
    # 判断现在这页前面和后面是否分别有五页
    ranges=[i for i in range(max(page-5,1),min(page+5,div)+1)]
    return render(request,'user_list.html',{'users':users,'ranges':ranges,'page':page})

def user_add(request):
    '''
    添加用户
    :param request:
    :return:
    '''
    if request.method=='GET':
        departs=Department.objects.all()
        return render(request,'user_add.html',{'departs':departs})
    else:
        name=request.POST.get('name')
        pwd=md5(request.POST.get('pwd'))
        age=request.POST.get('age')
        account=request.POST.get('account')
        create_time=request.POST.get('create_time')
        depart=request.POST.get('depart')
        sex=request.POST.get('sex')
        UserInfo.objects.create(name=name,password=pwd,age=age,account=account,create_time=create_time,depart_id=depart,sex=sex,ip='127.0.0.1')
        return redirect('/user/')

def user_delete(request):
    '''
    删除用户
    :param request:
    :return:
    '''
    id=request.GET.get('id')
    UserInfo.objects.filter(id=id).delete()
    return redirect("/user/")

def user_edit(request):
    '''
    编辑用户
    :param request:
    :return:
    '''
    if request.method=='GET':
        id=request.GET.get('id')
        # 需要注意取出遍历queryset的元素才可以获得下面的获取值的结果
        user=UserInfo.objects.filter(id=id).first()
        return render(request,'user_edit.html',{'user':user})
    else:
        print(request.POST)
        id=request.POST.get('id')
        name=request.POST.get('name')
        pwd=md5(request.POST.get('pwd'))
        UserInfo.objects.filter(id=id).update(name=name,password=pwd)
        return redirect("/user/")