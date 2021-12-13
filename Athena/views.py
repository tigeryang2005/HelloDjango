import json
import logging

import requests
from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from rest_framework import viewsets

from Athena.forms import StockInfoForm, UserForm, RegisterForm
from Athena.serializers import StockInfoSerializer
from Athena.serializers import UserSerializer, GroupSerializer
from .models import StockInfo, Stock

logger = logging.getLogger('log')


# Create your views here.
class StockInfoViewSet(viewsets.ModelViewSet):
    """
        此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。

    """
    queryset = StockInfo.objects.all()
    serializer_class = StockInfoSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permission.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    允许组查看或编辑的API路径。
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class Logout(View):
    def get(self, request):
        if not request.session.get('is_login', None):
            return redirect('login')
        # request.session.flush()
        # flush会一次性清空session中所有内容，可以使用下面的方法
        del request.session['is_login']
        del request.session['user_id']
        del request.session['user_name']
        logout(request)
        return redirect('login')


class Login(View):
    def get(self, request):
        next_url = request.GET.get('next', '')
        user_form = UserForm()
        context = {'next_url': next_url, 'user_form': user_form}
        return render(request, 'athena_templates/login.html', context=context)

    def post(self, request):
        if request.session.get('is_login', None):
            return redirect('stock_index')
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            path = request.POST.get('next_url', '')
            if user is not None:
                login(request, user)
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                if not path:
                    path = 'stock_index'
                    return redirect(reverse(path))
                else:
                    return redirect(path)
            else:
                msg = '用户名或密码错误'
                user_form = UserForm()
                return render(request, 'athena_templates/login.html', locals())
        else:
            msg = login_form.errors
            user_form = UserForm()
            return render(request, 'athena_templates/login.html', locals())


class Register(View):
    def get(self, request):
        register_from = RegisterForm()
        return render(request, 'athena_templates/register.html', locals())

    def post(self, request):
        register_from = RegisterForm(request.POST)
        if register_from.is_valid():
            username = register_from.cleaned_data['username']
            password = register_from.cleaned_data['password']
            confirm_password = register_from.cleaned_data['confirm_password']
            user = User.objects.create_user(username=username, password=password, email='test@test.com')
            user.save()
            msg = '用户名:{username}已注册成功！'.format(username=user.username)
            register_from = RegisterForm()
            return render(request, 'athena_templates/register.html', locals())
        else:
            msg = register_from.errors
            register_from = RegisterForm()
            return render(request, 'athena_templates/register.html', locals())


class StockInfoView(LoginRequiredMixin, View):
    def get(self, request):
        # 获取数据
        data = request.GET.dict()
        logger.info('前端发来的请求：' + json.dumps(data))
        # 后端分页 暂时不用
        # page_number = data.get('pageNumber', 1)
        # page_size = data.get('pageSize')
        # sort_name = data.get('sortName', 'date')
        # sort_order = data.get('sortOrder', 'asc')
        # if sort_order == 'asc':
        #     sort_order = ''
        # else:
        #     sort_order = '-'
        # if not data.get('pageNumber'):
        #     data.pop('pageNumber')
        # if not data.get('pageSize'):
        #     data.pop('pageSize')
        url = 'https://q.stock.sohu.com/hisHq'
        response = requests.get(url=url, params=data)
        content = json.loads(response.text)
        logger.info('搜狐返回数据：' + response.text)
        # 数据入库
        key_list = []
        for s in StockInfo._meta.fields:
            key_list.append(s.name)
        key_list = key_list[1:]
        stock_info_list = []
        for c in content:
            if c['status'] == 0:
                for h in c['hq']:
                    h.insert(0, c['code'])
                    stock_info_dict = dict(zip(key_list, h))
                    stock = Stock.objects.get(cn_code=c['code'])
                    stock_info_dict['code'] = stock
                    stock_info = StockInfo(**stock_info_dict)
                    stock_info_list.append(stock_info)
        StockInfo.objects.bulk_create(stock_info_list, ignore_conflicts=True)
        # 查询数据返回前端
        start_date = data['start'][0:4] + '-' + data['start'][4:6] + '-' + data['start'][6:8]
        end_date = data['end'][0:4] + '-' + data['end'][4:6] + '-' + data['end'][6:8]
        stock = Stock.objects.get(cn_code=data['code'])
        stock_info_query_set = stock.stockinfo_set.filter(date__gte=start_date) \
            .filter(date__lte=end_date).all()
        # stock_query_set_page = Paginator(stock_query_set, page_size).page(page_number).object_list
        res_dict = {}
        res_rows = []
        stocks = serializers.serialize('json', stock_info_query_set)
        stocks = json.loads(stocks)
        for s in stocks:
            s['fields']['id'] = s['pk']
            s['fields']['code'] = stock.code
            res_rows.append(s['fields'])
        res_dict['msg'] = 'success'
        res_dict['total'] = len(stock_info_query_set)
        res_dict['rows'] = res_rows
        res = json.dumps(res_dict)
        logger.info('返回前端数据：' + res)
        return HttpResponse(res)

    def post(self, request):
        data = json.loads(request.body)
        logger.info('前端发来的请求：' + json.dumps(data))
        stock_form = StockInfoForm(data)
        # 表单验证
        if stock_form.is_valid():
            res_data = [data]
            stock = stock_form.save()
            data['id'] = stock.id
            logger.info(serializers.serialize('json', [stock]))
            res = {'msg': "success", 'data': res_data}
        else:
            res = {'msg': "failed", 'data': stock_form.errors}

        res = json.dumps(res, ensure_ascii=False)
        logger.info('增加后的数据为:' + res)
        return HttpResponse(res)

    def put(self, request):
        data = json.loads(request.body)
        logger.info('前端发来的请求：' + json.dumps(data))
        stock_info = StockInfo.objects.get(pk=data.get('id'))
        # stock_info.code = Stock.objects.get(code=data.get('code'))
        data['code'] = stock_info.code
        stock_info_form = StockInfoForm(data, instance=stock_info)
        if stock_info_form.is_valid():
            res_data = data
            res_data['code'] = stock_info_form.instance.code.id
            stock_info = stock_info_form.save()
            logger.info(serializers.serialize('json', [stock_info]))
            res = {'msg': "success", 'data': res_data}
        else:
            res = {'msg': "failed", 'data': stock_info_form.errors}

        res = json.dumps(res, ensure_ascii=False)
        logger.info("更新后的数据为：" + res)
        return HttpResponse(res)

    def delete(self, request):
        data = json.loads(request.body)
        logger.info('前端发来的请求：' + request.body)
        StockInfo.objects.filter(id__in=data).delete()
        res = json.dumps(data)
        logger.info("删除的数据id为：" + res)
        return HttpResponse(res)


class StockIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'athena_templates/stock.html'
    http_method_names = ['get']

    # def get_context_data(self, **kwargs):
    #     # context = super().get_context_data(**kwargs)
    #     context = {}
    #     stocks = Stock.objects.all()[:10]
    #     context['msg'] = 'success'
    #     context['total'] = len(stocks)
    #     context['rows'] = stocks
    #     logger.info(context)
    #     return context


