from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from Athena.views import StockIndexView, StockInfoView, Login, Register, Logout, StockInfoViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
# 用router 没有api的版本号
# router.register(r'stock', views.StockViewSet)

stock_list = StockInfoViewSet.as_view({
     'get': 'list',
     'post': 'create'
})

stock_detail = StockInfoViewSet.as_view({
     'get': 'retrieve',
     'put': 'update',
     'patch': 'partial_update',
     'delete': 'destroy'
})

# 使用自动URL路由连接我们的API。
# 另外，我们还包括支持浏览器浏览API的登录URL。
urlpatterns = [
     url(r'^api/athena/1.0/stocks/$', stock_list, name='stock-list'),
     url(r'^api/athena/1.0/stocks/(?P<pk>[0-9]+)/$', stock_detail, name='stock-detail'),
     # url(r'^api/athena/1.0/stocks/$', views.stock_list),
     # url(r'^api/athena/1.0/stocks/(?P<pk>[0-9]+)/$', views.stock_detail),
     url(r'^', include(router.urls)),
     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
     path('accounts/login/', Login.as_view(), name='login'),
     path('register/', Register.as_view(), name='register'),
     path('logout/', Logout.as_view(), name='logout'),
     path('stock/index/', StockIndexView.as_view(), name='stock_index'),
    path('stock/', StockInfoView.as_view(), name='stock'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
