import json

from django.core.paginator import Paginator
from django.forms.models import model_to_dict
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.core import serializers
from django.db import transaction
from . import models
import time
import os
import traceback
import logging

from .models import Stock

logger = logging.getLogger('log')


# Create your views here.
@transaction.atomic
def del_stock(request):
    data = json.loads(request.body)
    Stock.objects.filter(id__in=data).delete()
    res = json.dumps(data)
    return HttpResponse(res)


@transaction.atomic
def add_stock(request):
    data = json.loads(request.body)
    data.pop('csrfmiddlewaretoken')
    stock = models.Stock(**data)
    stock.save()
    data['id'] = stock.pk
    res = [data]
    return HttpResponse(json.dumps(res))


@transaction.atomic
def stock_find(request):
    # 获取数据
    data = request.GET.dict()
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
    for s in Stock._meta.fields:
        key_list.append(s.name)
    key_list = key_list[1:]
    stock_list = []
    for c in content:
        if c['status'] == 0:
            for h in c['hq']:
                h.insert(0, c['code'])
                stock_dict = dict(zip(key_list, h))
                stock = Stock(**stock_dict)
                stock_list.append(stock)
    Stock.objects.bulk_create(stock_list, ignore_conflicts=True)
    # 查询数据返回前端
    start_date = data['start'][0:4] + '-' + data['start'][4:6] + '-' + data['start'][6:8]
    end_date = data['end'][0:4] + '-' + data['end'][4:6] + '-' + data['end'][6:8]
    stock_query_set = Stock.objects.filter(date__gte=start_date).filter(date__lte=end_date).all()
    # stock_query_set_page = Paginator(stock_query_set, page_size).page(page_number).object_list
    res_dict = {}
    res_rows = []
    stocks = serializers.serialize('json', stock_query_set)
    stocks = json.loads(stocks)
    for s in stocks:
        s['fields']['id'] = s['pk']
        res_rows.append(s['fields'])
    res_dict['status'] = 'success'
    res_dict['total'] = len(stock_query_set)
    res_dict['rows'] = res_rows
    res = json.dumps(res_dict)
    logger.info('返回前端数据：' + res)
    return HttpResponse(res)


def stock_index(request):
    return render(request, 'athena_templates/stock.html')


def update_book(request):
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    # 判断是否更新图片
    file = request.FILES.get('img_url', None)
    book = models.Books.objects.get(id=data.get('id'))
    if file:
        file_name = img_upload(data, request)
        if file_name:
            data['img_url'] = file_name[1:]
        else:
            data.pop('img_url')
        os.remove('.' + book.img_url)
    else:
        data['img_url'] = book.img_url
    models.Books.objects.filter(id=data.get('id')).update(**data)

    return HttpResponse('更新')


def edit_book(request):
    id = request.GET.get('id')
    book = models.Books.objects.get(id=id)
    return render(request, 'books/edit.html', {'book': book})


def del_book(request, book_id):
    try:
        book = models.Books.objects.get(id=book_id)
        os.remove('.' + book.img_url)
        book.delete()
    except:
        logger.error(traceback.format_exc())
    return redirect('list_book')


def list_book(request):
    data = models.Books.objects.all()
    context = {'data': data}
    return render(request, 'books/list.html', context)


def add_book(request):
    # 判断当前的请求方式，如果是get只返回html 如果是post则添加数据
    if request.method == 'GET':
        return render(request, 'books/add.html')
    else:
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')

        # 处理上传的文件
        img_url = img_upload(data, request)
        if img_url:
            data['img_url'] = img_url[1:]
        else:
            data.pop('img_url')

        try:
            book = models.Books(**data)
            book.save()
            return redirect(reverse('list_book'))
        except:
            os.remove(img_url)
            logger.error(traceback.format_exc())
            return redirect(reverse('add_book'), {'add_failed': '添加数据失败'})


def img_upload(data, request):
    file = request.FILES.get('img_url', None)
    if file:
        file_path = './static/uploads/' + data.get('name') + str(int(time.time())) + '.' + file.name.split('.').pop()
        try:
            with open(file_path, mode='wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            return file_path
        except:
            logger.error(traceback.format_exc())
            return None
    else:
        return None


def demo(request):
    # 添加数据的一种方式
    # student = models.Student()
    # student.name = '张三'
    # student.age = 24
    # student.sex = '1'
    # student.address = '天津'
    # s = student.save()
    # print(s, type(s))
    # 添加数据的另一种方式
    # data = {'name': '李四', 'age': 21, 'sex': '0', 'address': '天津'}
    # student = models.Student(**data)
    # student.save()
    # 查询数据
    # data = models.Student.objects.all()
    # print(data)
    # for s in data:
    #     print(s.name)
    # data = models.Student.objects.get(pk=1)
    # print(data.name)
    # data = models.Student.objects.filter(sex='0')
    # for s in data:
    #     print(s.sex)
    # student_data = {
    #     'name': '王五',
    #     'age': 18,
    #     'sex': '0',
    #     'address': '山西'
    # }
    # # 一对一模型添加
    # student = models.Student(**student_data)
    # student.save()
    # student = models.Student.objects.get(pk=2)
    # student_info = {
    #     'sid': student,
    #     'xueli': '硕士',
    #     'phone': '13888888888'
    # }
    # student_info_obj = models.StuInfo(**student_info)
    # student_info_obj.save()
    # student = models.Student.objects.first()
    # print(student.name)
    # print(student.stuinfo.phone)
    # student_info = models.StuInfo.objects.first()
    # print(student_info.xueli)
    # print(student_info.sid.name)
    # 一对多关系  存
    # b_obj = models.BanJi(name='二班')
    # b_obj.save()
    #
    # student = models.Student(name='赵六', bid=b_obj)
    # student.save()
    # 一对多关系 查询
    # b_obj = models.BanJi.objects.first()
    # print(b_obj.name)
    # print(b_obj.student_set.all())
    # for s in b_obj.student_set.all():
    #     print(s.name)
    #     print(s.stuinfo.xueli)
    #     print(s.bid.name)
    # 添加多对多关系
    # t1 = models.Teacher(name='王老师')
    # t2 = models.Teacher(name='张老师')
    # t1.save()
    # t2.save()
    # b_objects = models.BanJi.objects.all()
    # t1.bid.set(b_objects)
    # b_object = models.BanJi.objects.last()
    # t2.bid.add(b_object)
    # s_obj = models.Student.objects.first()
    # print(s_obj.bid.name)
    # 多对多查询
    print(models.Teacher.objects.first().bid.all())
    print(models.BanJi.objects.last().teacher_set.all())
    return render(request, 'athena_templates/demo.html')


# 字符串返回
def hello_world(request):
    return HttpResponse('hello world!')


# 模板返回
def index(request):
    return render(request, 'athena_templates/index.html', {'welcome': 'hello'})


# 接收url中的一部分参数
def index_year(request, year):
    return render(request, 'athena_templates/index.html', {'year': year})


def index_year_month(request, year, month):
    return render(request, 'athena_templates/index.html', {'year': year, 'month': month})
