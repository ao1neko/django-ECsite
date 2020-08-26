from django import forms
from django.core.mail import EmailMessage

from .models import Commodity,Company,CustomUser


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
class CommodityCreateForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = ("title", "content", "photo", "price") 

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
