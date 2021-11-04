from django.urls import path, re_path
from . import views

urlpatterns = [
     path('stock/', views.stock_index, name='stock_index'),
     path('stock/find', views.stock_find),
     path('book/update/', views.update_book, name='update_book'),
     path('book/edit/', views.edit_book, name='edit_book'),
     re_path(r'book/del/(?P<book_id>\d+)/', views.del_book, name='del_book'),
     re_path('book/add/', views.add_book, name='add_book'),
     path('book/list', views.list_book, name='list_book'),
     path('', views.hello_world),
     re_path('^demo/$', views.demo, name='demo'),
     re_path('^index/$', views.index),
     re_path(r'^index/(?P<year>[0-9]{4})/$', views.index_year),
     re_path(r'^index/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.index_year_month, name='index_year_month'),
]
