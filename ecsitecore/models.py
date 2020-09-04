import uuid
from django.db import models
from accounts.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

#TODO mapping自動生成,データ挿入script書く
class Commodity(models.Model):
    ACTIVE = (
        ('Y', 'active'),
        ('N', 'not_active'),
    )
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)#多対一
    title = models.CharField(verbose_name='商品名', max_length=40)
    content = models.TextField(verbose_name='商品概要', blank=True, null=True)
    photo = models.ImageField(verbose_name='写真', blank=True, null=True)
    price = models.IntegerField(verbose_name='値段', )
    is_active =  models.CharField(verbose_name='有効', max_length=40, choices=ACTIVE)
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
    num=models.IntegerField(verbose_name="数量", default=1)

    class Meta:
        verbose_name_plural = '取引'

    #クラスを参照時に返したい文字列
    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)#多対一
    commodity = models.ForeignKey(Commodity, verbose_name='商品', on_delete=models.PROTECT)#多対一
    content = models.TextField(verbose_name='内容', default="")
    score = models.IntegerField(verbose_name='スコア',validators=[MinValueValidator(1), MaxValueValidator(5)],default=3)
    created_at = models.DateTimeField(verbose_name='作成日時', blank=True, null=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'レビュー'

    #クラスを参照時に返したい文字列
    def __str__(self):
        return self.content

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)#多対一
    commodity = models.ForeignKey(Commodity, verbose_name='商品', on_delete=models.PROTECT)#多対一
    num = models.IntegerField(verbose_name='数量', default=0)
    
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
    tel_number_regex = RegexValidator(regex=r'^[0-9]+$', message = ("Tel Number must be entered in the format: '09012345678'. Up to 15 digits allowed."))
    phon= models.CharField(validators=[tel_number_regex], max_length=15, verbose_name='電話番号')
    created_at = models.DateTimeField(verbose_name='作成日時', blank=True, null=True, auto_now_add=True)

