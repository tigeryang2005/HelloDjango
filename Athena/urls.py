from django.urls import path, re_path
from . import views

urlpatterns = [
     path('', views.hello_world),
     re_path('^index/$', views.index),
     re_path(r'^index/(?P<year>[0-9]{4})/$', views.index_year),
     re_path(r'^index/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.index_year_month, name='index_year_month'),
]
