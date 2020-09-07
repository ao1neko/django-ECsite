import os
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from django.test.client import Client

from ..models import Commodity,CustomUser

#関数の最初にtestとつける




class LoggedInTestCase(TestCase):
    """各テストクラスで共通の事前準備処理をオーバーライドした独自TestCaseクラス"""

    def setUp(self):
        """テストメソッド実行前の事前設定"""

        # テストユーザーのパスワード
        self.password = os.environ.get('DB_PASSWORD')

        # 各インスタンスメソッドで使うテスト用ユーザーを生成し
        # インスタンス変数に格納しておく
        self.test_user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@exampl.com',
            password=self.password)
        # テスト用ユーザーでログインする
        self.client.login(email=self.test_user.email, password=self.password)



class TestUserInquiryView(LoggedInTestCase):
    def test_inquiry_success(self):
        params = {'title': 'test株式会社',
                  'phon': '000-0000-0000',}
        response = self.client.post(reverse_lazy('ecsitecore:profile-inquiries'), params)# Postを実行
        #self.assertRedirects(response, reverse_lazy('ecsitecore:ecsite-mylist'))#リスポンスを引数にリダイレクトを検証
     


