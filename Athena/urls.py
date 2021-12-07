from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.conf.urls import url, include
from rest_framework import routers
from Athena.views import StockIndexView, StockView, Login, Register, Logout
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# 使用自动URL路由连接我们的API。
# 另外，我们还包括支持浏览器浏览API的登录URL。
urlpatterns = [
     url(r'^', include(router.urls)),
     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
     path('accounts/login/', Login.as_view(), name='login'),
     path('register/', Register.as_view(), name='register'),
     path('logout/', Logout.as_view(), name='logout'),
     path('stock/index/', StockIndexView.as_view(), name='stock_index'),
     path('stock/', StockView.as_view(), name='stock'),
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
