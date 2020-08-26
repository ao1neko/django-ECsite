import uuid
from django.db import models
from accounts.models import CustomUser

class Commodity(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)#多対一
    title = models.CharField(verbose_name='タイトル', max_length=40)
    content = models.TextField(verbose_name='内容', blank=True, null=True)
    photo = models.ImageField(verbose_name='写真', blank=True, null=True)
    price = models.IntegerField(verbose_name='値段', )
    is_active =  models.CharField(verbose_name='有効', max_length=40)
    created_at = models.DateTimeField(verbose_name='作成日時', blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='作成日時', blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name_plural = '商品'

    #クラスを参照時に返したい文字列
    def __str__(self):
        return self.title

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)#多対一
    commodity = models.ForeignKey(Commodity, verbose_name='商品', on_delete=models.PROTECT)#多対一
    created_at = models.DateTimeField(verbose_name='作成日時', blank=True, null=True, auto_now_add=True)
    

    class Meta:
        verbose_name_plural = '取引'

    #クラスを参照時に返したい文字列
    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)#多対一
    commodity = models.ForeignKey(Commodity, verbose_name='商品', on_delete=models.PROTECT)#多対一
    content = models.TextField(verbose_name='内容', blank=True, null=True)
    star = models.IntegerField(verbose_name='星', )

    class Meta:
        verbose_name_plural = 'レビュー'

    #クラスを参照時に返したい文字列
    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)#多対一
    commodity = models.ForeignKey(Commodity, verbose_name='商品', on_delete=models.PROTECT)#多対一
    
    class Meta:
        verbose_name_plural = 'ショッピングカート'


class Library(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)#多対一
    commodity = models.ForeignKey(Commodity, verbose_name='商品', on_delete=models.PROTECT)#多対一
    
    class Meta:
        verbose_name_plural = 'お気に入り'
    

class Company(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)#多対一
    title = models.CharField(verbose_name='タイトル', max_length=40)
    phon = models.IntegerField(verbose_name='電話番号', )
    created_at = models.DateTimeField(verbose_name='作成日時', blank=True, null=True, auto_now_add=True)
