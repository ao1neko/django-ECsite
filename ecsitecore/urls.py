
from django.urls import path
from . import views
app_name = 'ecsitecore'
#appURL
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('list/', views.CommodityListView.as_view(), name='commodity-list'),
    path('list/<int:pk>/', views.commodityDetailView.as_view(), name='commodity-detail'),
    path('list-update/<int:pk>/', views.commodityUpdateView.as_view(), name='ecsite-update'),
    path('transaction/', views.TransactionsView.as_view(), name='transaction'),
    path('inquiries/', views.CommodityInquiryView.as_view(), name='ecsite-inquiries'),
    path('mylist/', views.MyCommodityListView.as_view(), name='ecsite-mylist'),
    path('profile/', views.ProfileView.as_view(), name='profile'),#スラグを使うにはViewに登録する
    path('profile-inquiries/', views.UserInquiryView.as_view(), name='profile-inquiries'),#スラグを使うにはViewに登録する
    path('profile/<slug:slug>', views.UserUpdateView.as_view(), name='profile-updates'),#スラグを使うにはViewに登録する
    path('mypage/', views.MyPageView.as_view(), name='mypage'),#スラグを使うにはViewに登録する
    path('company-mypage/', views.CompanyMyPageView.as_view(), name='company-mypage'),#スラグを使うにはViewに登録する
]

