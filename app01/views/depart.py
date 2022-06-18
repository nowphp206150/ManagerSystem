from django.shortcuts import render,redirect
from app01.models import Department

def depart_add(request):
    '''
    部门添加
    :param request:
    :return:
    '''
    if request.method=='GET':
        return render(request,'depart_add.html')
    else:
        title=request.POST.get('title')
        Department.objects.filter().create(title=title)
        return redirect('/depart/')

def depart_list(request):
    '''
    显示部门信息
    :return:
    '''
    page=request.GET.get('page')
    departs=Department.objects.filter()
    div,duo=divmod(departs.count(),8)
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
    end=min(end,departs.count())
    departs=departs[start:end+1]
    # 判断现在这页前面和后面是否分别有五页
    ranges=[i for i in range(max(page-5,1),min(page+5,div)+1)]
    return render(request,'depart_list.html',{'departs':departs,'ranges':ranges,'page':page})

def depart_edit(request):
    '''
    编辑部门的信息
    :param request:
    :return:
    '''
    if request.method=='GET':
        id=request.GET.get('id')
        depart=Department.objects.filter(id=id).first()
        return render(request,'depart_edit.html',{'depart':depart})
    else:
        id=request.POST.get('id')
        title=request.POST.get('title')
        Department.objects.filter(id=id).update(title=title)
        return redirect('/depart/')

def depart_delete(request):
    '''
    删除指定部门
    :param request:
    :return:
    '''
    id=request.GET.get('id')
    Department.objects.filter(id=id).delete()
    return redirect('/depart/')
