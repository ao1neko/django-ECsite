import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

#from .forms import InquiryForm, DiaryCreateForm
from .models import Commodity,CustomUser


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


class MyPageView(generic.TemplateView):
    template_name = "mypage.html"


class UserDetailView(generic.DetailView):
    model = CustomUser
    template_name = 'user_profile.html'
