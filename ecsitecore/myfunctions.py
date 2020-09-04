import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.core.validators import RegexValidator


def button_type_redirect(request,word):
    request.session['words'] = request.session.pop('words_store',None)
    request.session['types']=word
    return redirect('ecsitecore:commodity-list')   
 
def change_dict_key(d, old_key, new_key, default_value=None):
    d[new_key] = d.pop(old_key, default_value)

def change_hits_list(hits):
    new_json=[]
    for hit in hits:
        change_dict_key(hit,'_id','id')
        change_dict_key(hit,'_source','source')
        new_json.append(hit)
    return new_json


    