import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import CommodityCreateForm, CompanyCreateForm, UserCreateForm
from .models import Commodity, CustomUser, Transaction, Library


logger = logging.getLogger(__name__)


class HomeView(generic.TemplateView):
    template_name = "home.html"


class CommodityListView(generic.ListView):
    model = Commodity
    template_name = 'ecsite_list.html'
    paginate_by = 2

    def get_queryset(self):
        commodities = Commodity.objects.all().order_by('-created_at')
        return commodities


class commodityDetailView(generic.DetailView):
    model = Commodity
    template_name = 'ecsite_detail.html'


class TransactionsView(generic.TemplateView):
    template_name = "transaction.html"


class CommodityInquiryView(generic.FormView):
    template_name = "ecsite_inquiry.html"
    form_class = CommodityCreateForm
    success_url = reverse_lazy('ecsitecore:ecsite_mylist')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


class MyCommodityListView(generic.ListView):
    model = Commodity
    template_name = 'ecsite_mylist.html'
    paginate_by = 2

    def get_queryset(self):
        commodities = Commodity.objects.all().order_by('-created_at')
        return commodities




class MyPageView(generic.TemplateView):
    template_name = "mypage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library_list'] = Library.objects.all()
        context['transaction_list'] = Transaction.objects.all()
        return context
    

class CompanyMyPageView(generic.TemplateView):
    template_name = "company_page.html"


class ProfileView(generic.TemplateView):
    template_name = 'user_profile.html'


class UserInquiryView(generic.FormView):
    template_name = "user_inquiry.html"
    form_class = CompanyCreateForm
    success_url = reverse_lazy('ecsitecore:profile')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
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
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の更新に失敗しました。")
        return super().form_invalid(form)
