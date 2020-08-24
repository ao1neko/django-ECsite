import uuid
from django.db import models
from accounts.models import CustomUser

class Commodity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)#多対一
    title = models.CharField(verbose_name='タイトル', max_length=40, choices=SHIRT_SIZES)
    content = models.TextField(verbose_name='内容', blank=True, null=True)
    photo = models.ImageField(verbose_name='写真', blank=True, null=True)
    price = models.IntegerField(verbose_name='値段', )

    class Meta:
        verbose_name_plural = '商品'

    #クラスを参照時に返したい文字列
    def __str__(self):
        return self.title
