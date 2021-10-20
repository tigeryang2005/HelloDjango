from django.urls import path, re_path
from . import views

urlpatterns = [
     re_path('book/add/', views.add_book, name='add_book'),
     re_path('book/list', views.list_book, name='list_book'),
     path('', views.hello_world),
     re_path('^demo/$', views.demo, name='demo'),
     re_path('^index/$', views.index),
     re_path(r'^index/(?P<year>[0-9]{4})/$', views.index_year),
     re_path(r'^index/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.index_year_month, name='index_year_month'),
]
