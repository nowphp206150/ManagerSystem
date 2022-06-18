"""django_day01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import user,depart,prettynum,account,order,chart

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',user.index),
    path('index/', user.index),
    path('register/',user.register),
    path('user/',user.user_list),
    path('user/add/',user.user_add),
    path('user/delete/',user.user_delete),
    path('user/edit/',user.user_edit),
    path('depart/',depart.depart_list),
    path('depart/add/',depart.depart_add),
    path('depart/delete/',depart.depart_delete),
    path('depart/edit/',depart.depart_edit),
    #  靓号管理
    path('prettynum/',prettynum.prettynum_list),
    path('prettynum/add/',prettynum.prettynum_add),
    path('prettynum/edit/',prettynum.prettynum_edit),
    path('prettynum/delete/',prettynum.prettynum_delete),
    path('login/',account.login),
    path('logout/',account.logout),
    path('imgcode/',account.imgcode),
    # 订单管理
    path('order/',order.order_list),
    path('order/add/',order.order_add),
    path('order/delete/',order.order_delete),
    path('order/edit/',order.order_edit),
    path('chart/',chart.chart_list),
]
