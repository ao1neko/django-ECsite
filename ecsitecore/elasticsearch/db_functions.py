#TODO DBとelasticsearch同期させる関数
from datetime import datetime
from elasticsearch import Elasticsearch
import sys
import argparse
import inspect
from .myelasticsearch import MyElasticSearch

def convert_dbto_elastic(Class,object,fileds):
    myjson={}
    for filed in fileds:
        model_filed_class = Class._meta.get_field(filed).__class__.__name__
        if model_filed_class == "CharField" or model_filed_class == 'TextField' or  model_filed_class == 'IntegerField' or  model_filed_class == 'ImageField':
            myjson[filed] = object.__dict__[filed]    
        elif model_filed_class == 'DateTimeField':
            time = object.__dict__[filed]
            myjson[filed] = time.strftime('%Y-%m-%dT%H:%M:%S')
        elif model_filed_class != 'AutoField':
            print("フィールドタイプが適切ではありません",model_filed_class)
            sys.exit(1)
    return myjson


def method_db(es,fields,object_list,method):
    bulk_list=[]
    index_name=es.index_name
    for i in object_list :
        tmp={}
        tmp['type']=method
        tmp['index_name']=index_name
        tmp['id']=i
        doc={}
        for f in fields:
            doc[f[0]]=f[1]
        tmp['doc']=doc
        bulk_list.append(tmp)
    es.bulk(bulk_list)


def create_db(Class,es,fields,**kwargs):
    objects.update(**kwargs)
    object_list = objects.values_list('id', flat=True)
    method_db(es,fields,object_list,"create")


def update_db(objects,es,fields,**kwargs):
    #objects.update(**kwargs)
    for k in kwargs:
        print(k)
    object_list = objects.values_list('id', flat=True)
    method_db(es,fields,object_list,"update")

