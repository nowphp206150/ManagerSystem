from django.shortcuts import render,redirect,HttpResponse
from django import forms
from django.core.validators import ValidationError
from app01.models import Admin
from app01.utils.check_code import check_code
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO

class LoginForm(forms.Form):
    name=forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password=forms.CharField(label='密码',widget=forms.PasswordInput(render_value=True,attrs={'class':'form-control'}))
    code=forms.CharField(label='验证码',widget=forms.TextInput(attrs={'class':'form-control','style':'width:175px;'}))

    def clean_name(self):
        name=self.cleaned_data['name']
        if name=='':
            raise ValidationError('请输入用户名')
        else:
            if Admin.objects.filter(name=name):
                return name
            else:
                raise ValidationError('用户不存在')
@csrf_exempt
def imgcode(request):
    '''
    刷新验证码
    :param request:
    :return:
    '''
    print(request.POST)
    img, code = check_code()
    with open('./app01/static/img/code.png', 'wb') as fp:
        img.save(fp, format='png')
    # 获得登陆页面表示用户还没登录，此时生成验证码并保存到session中
    request.session['code'] = code
    #  设置好session保存的时间，变相的设置了用户登录和验证码存活的时间
    request.session.set_expiry(60)
    return HttpResponse('验证码生成成功')

def login(request):
    '''
    登录界面
    :param request:
    :return:
    '''

    if request.method=="GET":
        form=LoginForm(request.GET)
        return render(request,'login.html',{'form':form})
    else:
        form=LoginForm(request.POST)
        if form.is_valid():
            admin=Admin.objects.filter(name=form.cleaned_data.get('name'),password=form.cleaned_data.get('password')).first()
            if admin:
                code_str=request.session.get('code')
                if code_str:
                    if form.cleaned_data.get('code') == code_str:
                        # 注册好用户信息，表示用户的登录成功
                        request.session['info'] = {'name': admin.name}
                        # 需要设置好session保存的时间，确保这几天免密登录，否则就是上面设置的60秒就清楚了
                        request.session.set_expiry(60*60*24*7)
                        return redirect('/index/')
                    else:
                        form.add_error('code', '验证码错误')
                        return render(request, 'login.html', {'form': form, 'error': form.errors})
                else:
                    form.add_error('code','验证码超时,请点击刷新')
                    return render(request, 'login.html', {'form': form, 'error': form.errors})
            else:
                form.add_error('password', '用户名或密码错误')
                return render(request, 'login.html', {'form': form, 'error': form.errors})
        else:
            return render(request,'login.html',{'form':form,'error':form.errors})

def logout(request):
    '''
    退出登录
    :param request:
    :return:
    '''
    # request.session获得当前登录状态的信息，后面直接清除
    request.session.clear()
    return redirect('/login/')