import uuid
from django.db import models
from accounts.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)#多対一
    commoditykey = models.IntegerField(verbose_name='商品番号')
    created_at = models.DateTimeField(verbose_name='作成日時', blank=True, null=True, auto_now_add=True)
    num=models.IntegerField(verbose_name="数量", default=1)

    class Meta:
        verbose_name_plural = '取引'

    #クラスを参照時に返したい文字列
    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)#多対一
    commoditykey = models.IntegerField(verbose_name='商品番号')
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
    commoditykey = models.IntegerField(verbose_name='商品番号')
    num = models.IntegerField(verbose_name='数量', default=0)
    
    class Meta:
        verbose_name_plural = 'ショッピングカート'


class Library(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)#多対一
    commoditykey = models.IntegerField(verbose_name='商品番号')

    class Meta:
        verbose_name_plural = 'お気に入り'
    

class Company(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)#多対一
    title = models.CharField(verbose_name='タイトル', max_length=40)
    tel_number_regex = RegexValidator(regex=r'^[0-9]+$', message = ("Tel Number must be entered in the format: '09012345678'. Up to 15 digits allowed."))
    phon= models.CharField(validators=[tel_number_regex], max_length=15, verbose_name='電話番号')
    created_at = models.DateTimeField(verbose_name='作成日時', blank=True, null=True, auto_now_add=True)

