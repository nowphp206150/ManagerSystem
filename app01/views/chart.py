from django.shortcuts import render
from django import forms

class MyForm(forms.Form):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    img=forms.FileField(widget=forms.FileInput())

def chart_list(request):
    '''
    展示图标
    :param request:
    :return:
    '''
    if request.method=='GET':
        form=MyForm()
        return render(request,'chart_list.html',{'form':form})
    else:
        form = MyForm(data=request.POST, files=request.FILES)

