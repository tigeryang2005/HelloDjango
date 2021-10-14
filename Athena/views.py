from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


# 字符串返回
def hello_world(request):
    return HttpResponse('hello world!')


# 模板返回
def index(request):
    return render(request, 'athena_templates/index.html')
