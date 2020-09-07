from django import forms
from django.core.mail import EmailMessage

from .models import Company,CustomUser, Cart, Review


#フォームをモデルから作成
class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "profile_text") 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


#フォームをモデルから作成
class CommodityCreateForm(forms.Form):
    title = forms.CharField(label='商品名', max_length=40)
    content = forms.CharField(label='商品概要',widget=forms.Textarea )
    photo = forms.ImageField(label='写真', )
    price = forms.IntegerField(label='値段', )
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


#フォームをモデルから作成
class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("title", "phon", ) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



#フォームをモデルから作成
class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("content", "score") 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['placeholder'] = ''
        self.fields['score'].widget.attrs['placeholder'] = '1~5の値を入力して下さい'



#フォームをモデルから作成
class CartCreateForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ("num", ) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
