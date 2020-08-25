from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    #_create_userは直接使わない
    def _create_user(self, username, email, password, **extra_fields):
        if not email :
            raise ValueError('The given email must be set')
        if not username :
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)#書き換えuser = self.model(username=username, email=email, date_of_birth=date_of_birth,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_user(self, username, email, password=None, **extra_fields):
        # admin の権限はないよ
        extra_fields.setdefault('is_staff', False)
        # 全権限は持たせないよ
        extra_fields.setdefault('is_superuser', False)
        # という状態でユーザモデル作るよ
        return self._create_user(username, email, password, **extra_fields)
    def create_superuser(self, username, email, password=None, **extra_fields):
        # admin に入れるよ
        extra_fields.setdefault('is_staff', True)
        # 全権限もってるよ
        extra_fields.setdefault('is_superuser', True)
        # superuser は権限をもってないといけないので 簡単に Model Validation するよ
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)
        
#username,first_name,last_name,email,is_staff(adminに参加できるか),is_active(Falseの時ログインできない),data_joined(アカウントの作成された時刻)
class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    profile_text = models.TextField(verbose_name='本文', blank=True, null=True)
    company_or_individual = models.CharField(verbose_name='会社', max_length=40,default='individual')#デフォルト指定


    objects=UserManager()#ハンドラー
    USERNAME_FIELD='email'#一意な値にするフィールド名
    REQUIRED_FIELDS = ['username']

    #管理画面で'CustomUser'という名前で表示される
    class Meta:
        verbose_name_plural = 'CustomUser'

