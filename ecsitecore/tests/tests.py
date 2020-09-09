import os
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from django.test.client import Client

from ecsitecore.elasticsearch.commoditydoc import CommodityDoc
from ecsitecore.myfunctions import *
from ..models import CustomUser,Review,Library,Cart,Company

#関数の最初にtestとつける




class LoggedInTestCase(TestCase):
    def setUp(self):
        self.commoditydoc=CommodityDoc()
        self.password = os.environ.get('DB_PASSWORD')
        self.test_user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@exampl.com',
            password=self.password,
            id=1)
        self.client.login(email=self.test_user.email, password=self.password)

class TestHomeView(TestCase):
    def test_home_success(self):
        params = {
             'search-text': '猫',
             'search-button':'',
            }
        response = self.client.post(reverse_lazy('ecsitecore:home'), params)
        self.assertRedirects(response, reverse_lazy('ecsitecore:commodity-list'))
        
    def test_home_fail(self):
        params = {
             'search-text': '',
             'search-button':'',
            }
        response = self.client.post(reverse_lazy('ecsitecore:home'), params)
        self.assertRedirects(response, reverse_lazy('ecsitecore:home'))

class TestCommodityListView(LoggedInTestCase):
    def test_list_get(self):
        response = self.client.get(reverse_lazy('ecsitecore:commodity-list'))
        self.assertEqual(response.context['mycommodity_list'], change_hits_list(self.commoditydoc.word_search()))
        
    def test_list_post_success(self):
        params={
            'price-button':''
        }
        response = self.client.post(reverse_lazy('ecsitecore:commodity-list'),params)
        self.assertRedirects(response, reverse_lazy('ecsitecore:commodity-list'))
        
class TestCommodityDeatailView(LoggedInTestCase):
    def test_library_success(self):
        self.assertEqual(Library.objects.all().count(),0)
        params={
            'library-button':''
        }
        id=self.commoditydoc.word_search()[0]['_id']
        response = self.client.post(reverse_lazy('ecsitecore:commodity-detail',kwargs={'slug': id}),params)
        self.assertEqual(Library.objects.all().count(),1)
        self.assertRedirects(response,reverse_lazy('ecsitecore:mypage'))

    def test_cart_success(self):
        params={
            'cart-button':'',
            'num':5
        }
        id=self.commoditydoc.word_search()[0]['_id']
        response = self.client.post(reverse_lazy('ecsitecore:commodity-detail',kwargs={'slug': id}),params)
        self.assertRedirects(response,reverse_lazy('ecsitecore:transaction'))

    def test_cart_fail(self):
        params={
            'cart-button':'',
        }
        id=self.commoditydoc.word_search()[0]['_id']
        response = self.client.post(reverse_lazy('ecsitecore:commodity-detail',kwargs={'slug': id}),params)
        self.assertFormError(response, 'form', 'num', 'このフィールドは必須です。')

    def test_review_fail(self):
        params={
            'review-button':'',
            'content':'test'
        }
        id=self.commoditydoc.word_search()[0]['_id']
        response = self.client.post(reverse_lazy('ecsitecore:commodity-detail',kwargs={'slug': id}),params)
        self.assertRedirects(response,reverse_lazy('ecsitecore:commodity-detail',kwargs={'slug': id}))

class TestCommodityUpdateView(LoggedInTestCase):
    def test_form_fail(self):
        param={
            'title':'猫',
            'content':'test',
            'price':10000,
        }
        id=self.commoditydoc.word_search()[0]['_id']
        response = self.client.post(reverse_lazy('ecsitecore:ecsite-update',kwargs={'slug':id}),param)# Postを実行
        self.assertFormError(response, 'form', 'photo', 'このフィールドは必須です。')



class TestTransactionView(LoggedInTestCase):
    def test_delete_success(self):
        params={
            'delete-button':1
        }
        Cart.objects.create(user=self.test_user,commoditykey="111",num=3,id=1)
        self.assertEqual(Cart.objects.all().count(),1)
        response = self.client.post(reverse_lazy('ecsitecore:transaction',),params)
        self.assertEqual(Cart.objects.all().count(),0)

        


class TestCommodityInquiryView(LoggedInTestCase):
    def test_form_fail(self):
        param={
            'title':'猫',
            'content':'test',
            'price':10000,
        }
        id=self.commoditydoc.word_search()[0]['_id']
        response = self.client.post(reverse_lazy('ecsitecore:ecsite-inquiries'),param)# Postを実行
        self.assertFormError(response, 'form', 'photo', 'このフィールドは必須です。')



class TestUserInquiryView(LoggedInTestCase):
    def test_user_success(self):
        params={
            'title':'会社',
            'phon':'08099998888'
        }
        response = self.client.post(reverse_lazy('ecsitecore:profile-inquiries'),params)
        self.assertRedirects(response,reverse_lazy('ecsitecore:profile'))

    def test_user_fail(self):
        params={
            'title':'会社',
        }
        response = self.client.post(reverse_lazy('ecsitecore:profile-inquiries'),params)
        self.assertFormError(response, 'form', 'phon', 'このフィールドは必須です。')


class TestUserUpdateView(LoggedInTestCase):
    def test_user_success(self):
        params={
            'username':'aoneko2',
            'email':'aoneko2@exampl.com',
            'profile_text':'test',
        }
        response = self.client.post(reverse_lazy('ecsitecore:profile-updates',kwargs={'slug':"testuser"}),params)
        self.assertRedirects(response,reverse_lazy('ecsitecore:profile'))

    def test_user_fail(self):
        params={
            'email':'aoneko2@exampl.com',
            'profile_text':'test',
        }
        response = self.client.post(reverse_lazy('ecsitecore:profile-updates',kwargs={'slug':'testuser'}),params)
        self.assertFormError(response, 'form', 'username', 'このフィールドは必須です。')

class TestMyPageView(LoggedInTestCase):
    def test_delete_success(self):
        params={
            'delete-button':1
        }
        Library.objects.create(user=self.test_user,commoditykey="111",id=1)
        self.assertEqual(Library.objects.all().count(),1)
        response = self.client.post(reverse_lazy('ecsitecore:mypage'),params)
        self.assertEqual(Library.objects.all().count(),0)
