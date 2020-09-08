import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.core.validators import RegexValidator
from django.db.models import Avg

from .myfunctions import *
from .elasticsearch.commoditydoc import CommodityDoc
from .forms import CommodityCreateForm, CompanyCreateForm, UserCreateForm, CartCreateForm, ReviewCreateForm
from .models import CustomUser, Transaction, Library,Cart, Review


commoditydoc = CommodityDoc()
logger = logging.getLogger(__name__)

class HomeView(generic.TemplateView):
    template_name = "home.html"
 
    def post(self, request, *args, **kwargs):
        if 'search-button' in request.POST:
            word=request.POST['search-text'] 
            if word == '':
                messages.error(self.request, '単語を入力して下さい。')
                return redirect('ecsitecore:home')   
            else:
                self.request.session['words']=word
                self.request.session.pop('words_store',None)
                return redirect('ecsitecore:commodity-list')   


class CommodityListView(generic.TemplateView):
    template_name = 'ecsite_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        word=self.request.session.pop('words', None)
        self.request.session['words_store']=word
        type=self.request.session.pop('types',None)
        if word==None:
            if type==None or type=="time":
                context['mycommodity_list'] =  change_hits_list(commoditydoc.word_search())
            elif type == 'price':
                context['mycommodity_list'] =  change_hits_list(commoditydoc.word_search(sort=CommodityDoc.price))
            elif type == 'order':
                context['mycommodity_list'] =  change_hits_list(commoditydoc.word_search(sort=CommodityDoc.order))    
            elif type == 'score':
                context['mycommodity_list'] =  change_hits_list(commoditydoc.word_search(sort=CommodityDoc.score))
        else:
            context['mycommodity_list'] =  change_hits_list(commoditydoc.word_search(sort=CommodityDoc.score,word=word))
        return context

    
    def post(self, request, *args, **kwargs):
        if 'time-button' in request.POST:
            return button_type_redirect(request,"time")
        elif 'price-button' in request.POST:
            return button_type_redirect(request,"price")
        elif 'order-button' in request.POST:
            return button_type_redirect(request,"order")
        elif 'score-button' in request.POST:
            return button_type_redirect(request,"score")
        elif 'search-button' in request.POST:
            request.session['words'] =request.POST['search-text'] 
            request.session.pop('words_store',None)
            return redirect('ecsitecore:commodity-list')   
        else:
            print(request.POST)
            return redirect('ecsitecore:commodity-list')   



class commodityDetailView(generic.FormView,):
    template_name = 'ecsite_detail.html'
    form_class = CartCreateForm

    def post(self, request, *args, **kwargs):
        if 'delete-button' in request.POST:
            commoditydoc.update(id=self.kwargs['slug'],body={"is_active":"not_active"})
            messages.success(self.request, '商品を削除しました。')
            return redirect('ecsitecore:ecsite-mylist')   
        elif 'delete-review-button' in request.POST:
            Review.objects.filter(pk=request.POST['delete-review-button']).delete()
            messages.success(self.request, 'レビューを削除しました。')
            return redirect(reverse_lazy('ecsitecore:commodity-detail', kwargs={'slug': self.kwargs['slug']}))
        elif 'library-button' in request.POST:
            Library.objects.get_or_create(user=request.user, commoditykey=self.kwargs['slug'])
            messages.success(self.request, 'お気に入りに追加しました。')
            return redirect('ecsitecore:mypage')   
        elif 'cart-button' in request.POST:
            form = self.get_form()
            if form.is_valid():
                num=form.cleaned_data['num']
                tmp=Cart.objects.filter(user=request.user, commoditykey=self.kwargs['slug'])
                if tmp.count()==0:
                    Cart.objects.create(user=request.user, commoditykey=self.kwargs['slug'],num=num)
                else:
                    tmp.update(num=num)
                messages.success(self.request, 'カートに追加しました。')
                return redirect('ecsitecore:transaction')
            else:
                return self.form_invalid(form)
        elif 'review-button' in request.POST:
            rform = ReviewCreateForm(**self.get_form_kwargs())
            # バリデーション
            if rform.is_valid():
                # フォームに書き込んだ部分を取得する(保存しない)
                rform_query = rform.save(commit=False)
                rform_query.user = request.user
                rform_query.commoditykey = self.kwargs['slug']
                # 保存
                rform_query.save()
                score=Review.objects.filter(commoditykey=self.kwargs['slug']).aggregate(Avg('score'))
                commoditydoc.update_document(id=self.kwargs['slug'],doc={"score":score})
                messages.success(self.request, 'レビューを追加しました。')
                return redirect(reverse_lazy('ecsitecore:commodity-detail', kwargs={'slug': self.kwargs['slug']}))
            else:
                messages.error(self.request, 'スコアは1~5の値を入力して下さい')
                return redirect(reverse_lazy('ecsitecore:commodity-detail', kwargs={'slug': self.kwargs['slug']}))
            
                    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_list'] = Review.objects.filter(commoditykey=self.kwargs['slug']).order_by("created_at")
        context['review_form'] = ReviewCreateForm()
        doc=commoditydoc.get_document(id=self.kwargs['slug'])
        context['myobject']={
            'title':doc['_source']['title'],
            'price':doc['_source']['price'],
            'content':doc['_source']['content'],
            'photo':doc['_source']['photo'],
            'userid':doc['_source']['userkey'],
            'id':doc['_id'],
        }
        return context

    

class commodityUpdateView(LoginRequiredMixin,generic.FormView):
    template_name = 'ecsite_update.html'
    form_class = CommodityCreateForm

    def get_success_url(self):
        return reverse_lazy('ecsitecore:commodity-detail', kwargs={'slug': self.kwargs['slug']})

    def form_valid(self, form):
        doc={
            "title":form.cleaned_data['title'],
            'content':form.cleaned_data['content'],
            'photo':"/media/"+form.cleaned_data['photo'],
            'price':form.cleaned_data['price']
        }
        commoditydoc.update_document(doc=doc,id=self.kwargs['slug'])
        messages.success(self.request, '商品情報を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "商品情報の更新に失敗しました。")
        return super().form_invalid(form)




import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
class TransactionsView(LoginRequiredMixin, generic.TemplateView):
    template_name = "transaction.html"
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        if "delete-button" in request.POST:
            Cart.objects.filter(pk=request.POST['delete-button']).delete()
            messages.success(self.request, 'カートから削除しました。')
            return redirect('ecsitecore:transaction')
        else:
            """購入時の処理"""
            token = request.POST['stripeToken']  # フォームでのサブミット後に自動で作られる
            sum=0 
            for carti in Cart.objects.filter(user=self.request.user):
                sum+=commoditydoc.get_document(id=carti.commoditykey)["price"]*carti.num
            try:
                # 購入処理
                charge = stripe.Charge.create(
                    amount=sum,
                    currency='jpy',
                    source=token,
                    description='メール:{}'.format(request.user.email),
                )
            except stripe.error.CardError as e:
                # カード決済が上手く行かなかった(限度額超えとか)ので、メッセージと一緒に再度ページ表示
                context = self.get_context_data()
                context['message'] = 'Your payment cannot be completed. The card has been declined.'
                return render(request, 'ecsitecore/transaction.html', context)
            else:
                # 上手く購入できた。Django側にも購入履歴を入れておく
                #TODO テスト
                tmp=Cart.objects.filter(user=self.request.user)
                for carti in tmp:
                    Transaction.objects.create(user=request.user,commoditykey=carti.commoditykey, num=carti.num)
                    commodity.update(id=carti.commoditykey,doc={"order":commodity.order+carti.num})
                tmp.delete()
                return redirect('ecsitecore:commodity-list')

    def get_context_data(self, **kwargs):
        """STRIPE_PUBLIC_KEYを渡したいだけ"""
        context = super().get_context_data(**kwargs)
        mycart_list=[]
        for cart in Cart.objects.filter(user=self.request.user):
            commoditykey=cart.commoditykey
            doc=commoditydoc.get_document(id=commoditykey)
            tmp={}
            tmp['commoditykey']=commoditykey
            tmp['photo']=doc['_source']['photo']
            tmp['title']=doc['_source']['title']
            tmp['price']=doc['_source']['price']
            tmp['num']=cart.num
            mycart_list.append(tmp)
        context['mycart_list'] = mycart_list
        context['publick_key'] = settings.STRIPE_PUBLIC_KEY
        sum=0 
        for carti in Cart.objects.filter(user=self.request.user):
            sum+=commoditydoc.get_document(id=carti.commoditykey)["_source"]["price"]*carti.num
        context['price_amount']=sum 
        return context

class CommodityInquiryView(LoginRequiredMixin,generic.FormView):
    template_name = "ecsite_inquiry.html"
    form_class = CommodityCreateForm
    success_url = reverse_lazy('ecsitecore:ecsite-mylist')

    def form_valid(self, form):
        commoditydoc.insert_document(userkey=self.request.user.id,title=form.cleaned_data['title'],content=form.cleaned_data['content'],photo=form.cleaned_data['photo']._get_name(),price=form.cleaned_data['price'])
        messages.success(self.request, '商品を陳列しました。')
        #TODO 数秒待たないといけない,elasticsearchに書込みが終わってない?
        # mylistのページに商品が表示されない
        return super().form_valid(form)


class MyCommodityListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'ecsite_mylist.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commodities"]= change_hits_list(commoditydoc.word_search())
        print(context['commodities'])
        return context




class MyPageView(LoginRequiredMixin,generic.TemplateView):
    template_name = "mypage.html"

    def post(self, request, *args, **kwargs):
        if "delete-button" in request.POST:
            Library.objects.filter(pk=request.POST['delete-button']).delete()
            messages.success(self.request, 'お気に入りから削除しました。')
            return redirect('ecsitecore:mypage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mylibrary_list=[]
        for cart in Library.objects.filter(user=self.request.user):
            commoditykey=cart.commoditykey
            doc=commoditydoc.get_document(id=commoditykey)
            tmp={}
            tmp['commoditykey']=commoditykey
            tmp['photo']=doc['_source']['photo']
            tmp['title']=doc['_source']['title']
            tmp['price']=doc['_source']['price']
            mylibrary_list.append(tmp)
        context['mylibrary_list'] = mylibrary_list
        context['transaction_list'] = Transaction.objects.filter(user=self.request.user)
        return context
    

class CompanyMyPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = "company_page.html"


class ProfileView(LoginRequiredMixin,generic.TemplateView):
    template_name = 'user_profile.html'


class UserInquiryView(LoginRequiredMixin, generic.FormView):
    template_name = "user_inquiry.html"
    form_class = CompanyCreateForm
    success_url = reverse_lazy('ecsitecore:profile')

    def form_valid(self, form):
        company = form.save(commit=False)
        company.user = self.request.user
        company.save()
        messages.success(self.request, '権限を申請しました。')
        return super().form_valid(form)


#更新なのでFOrmも必要最低限でいい
class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    template_name = 'user_update.html'
    form_class = UserCreateForm
    slug_field="username"#スラグに使うフィールド名
    slug_url_kwarg="slug"#slugにしておく 変数名_ur_kwarg=フィールド名

    def get_success_url(self):
        return reverse_lazy('ecsitecore:profile')

    def form_valid(self, form):
        messages.success(self.request, '情報を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "情報の更新に失敗しました。")
        return super().form_invalid(form)
