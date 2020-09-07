import os
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from django.test.client import Client

from ..models import CustomUser

#関数の最初にtestとつける




class LoggedInTestCase(TestCase):
    def setUp(self):
        self.password = os.environ.get('DB_PASSWORD')
        self.test_user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@exampl.com',
            password=self.password)
        self.client.login(email=self.test_user.email, password=self.password)



class TestHomeView(TestCase):
    def test_home_success(self):
        params = {
             'search-text': '猫',
            }
        response = self.client.post(reverse_lazy('ecsitecore:home'), params)
        self.assertRedirects(response, reverse_lazy('ecsitecore:commodity-list'))
        
    def test_home_fail(self):
        params = {
             'search-text': '',
            }
        response = self.client.post(reverse_lazy('ecsitecore:home'), params)
        self.assertRedirects(response, reverse_lazy('ecsitecore:home'))

class TestCommodityListView(TestCase):
    def test_inquiry_success(self):
        response = self.client.get(reverse_lazy('ecsitecore:profile-inquiries'))# Postを実行
        
class TestCommodityDeatailView(LoggedInTestCase):
    def test_inquiry_success(self):
        response = self.client.get(reverse_lazy('ecsitecore:profile-inquiries'))# Postを実行
        
class TestCommodityUpdateView(LoggedInTestCase):
    def test_inquiry_success(self):
        response = self.client.get(reverse_lazy('ecsitecore:profile-inquiries'))# Postを実行
        #self.assertRedirects(response, reverse_lazy('ecsitecore:ecsite-mylist'))#リスポンスを引数にリダイレクトを検証
class TestTransactionView(LoggedInTestCase):
    def test_inquiry_success(self):
        response = self.client.get(reverse_lazy('ecsitecore:profile-inquiries'))# Postを実行
        #self.assertRedirects(response, reverse_lazy('ecsitecore:ecsite-mylist'))#リスポンスを引数にリダイレクトを検証
class TestCommodityInquiryView(LoggedInTestCase):
    def test_inquiry_success(self):
        response = self.client.get(reverse_lazy('ecsitecore:profile-inquiries'))# Postを実行
        #self.assertRedirects(response, reverse_lazy('ecsitecore:ecsite-mylist'))#リスポンスを引数にリダイレクトを検証
class TestMyCommodityListView(LoggedInTestCase):
    def test_inquiry_success(self):
        response = self.client.get(reverse_lazy('ecsitecore:profile-inquiries'))# Postを実行
        #self.assertRedirects(response, reverse_lazy('ecsitecore:ecsite-mylist'))#リスポンスを引数にリダイレクトを検証
class TestProfileView(LoggedInTestCase):
    def test_inquiry_success(self):
        response = self.client.get(reverse_lazy('ecsitecore:profile-inquiries'))# Postを実行
        #self.assertRedirects(response, reverse_lazy('ecsitecore:ecsite-mylist'))#リスポンスを引数にリダイレクトを検証
class TestUserInquiryView(LoggedInTestCase):
    def test_inquiry_success(self):
        response = self.client.get(reverse_lazy('ecsitecore:profile-inquiries'))# Postを実行
        #self.assertRedirects(response, reverse_lazy('ecsitecore:ecsite-mylist'))#リスポンスを引数にリダイレクトを検証
class TestUserUpdateView(LoggedInTestCase):
    def test_inquiry_success(self):
        response = self.client.get(reverse_lazy('ecsitecore:profile-inquiries'))# Postを実行
        #self.assertRedirects(response, reverse_lazy('ecsitecore:ecsite-mylist'))#リスポンスを引数にリダイレクトを検証
class TestMyPageView(LoggedInTestCase):
    def test_inquiry_success(self):
        response = self.client.get(reverse_lazy('ecsitecore:profile-inquiries'))# Postを実行
        #self.assertRedirects(response, reverse_lazy('ecsitecore:ecsite-mylist'))#リスポンスを引数にリダイレクトを検証
class TestCompanyMyPageView(LoggedInTestCase):
    def test_inquiry_success(self):
        response = self.client.get(reverse_lazy('ecsitecore:profile-inquiries'))# Postを実行
        #self.assertRedirects(response, reverse_lazy('ecsitecore:ecsite-mylist'))#リスポンスを引数にリダイレクトを検証
