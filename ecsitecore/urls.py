
from django.urls import path
from . import views
app_name = 'ecsitecore'
#appURL
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('list/', views.CommodityListView.as_view(), name='commodity-list'),
    path('list/<int:pk>/', views.commodityDetailView.as_view(), name='commodity-detail'),
    path('publish/', views.HomeView.as_view(), name='ecsite-publish'),
    path('published/', views.HomeView.as_view(), name='ecsite-published'),
    path('profile/<slug:slug>/', views.HomeView.as_view(), name='profile'),#スラグを使うにはViewに登録する
    path('mypage/<slug:slug>/', views.HomeView.as_view(), name='mypage'),#スラグを使うにはViewに登録する
    path('company-mypage/<slug:slug>/', views.HomeView.as_view(), name='company-mypage'),#スラグを使うにはViewに登録する


]
