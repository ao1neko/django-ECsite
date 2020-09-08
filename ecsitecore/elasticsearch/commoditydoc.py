from datetime import datetime
from elasticsearch import Elasticsearch
import sys
import argparse
import inspect
from .myelasticsearch import MyElasticSearch

class CommodityDoc(MyElasticSearch):
    created_at={
        "created_at":{
            "order":"desc"
        }
    }
    price={
        "price":{
            "order":"asc"
        }
    }
    order={
        "order":{
            "order":"desc"
        }
    }
    score={
        "score":{
            "order":"desc"
        }
    }

    def __init__(self,index_name='commodity'):
        self.mappings ={
            "properties": {
                "userkey":{
                    "type":"integer",
                },
                "title":{
                    "type":"text",
                    "analyzer":"my_analyzer",
                    "fielddata":True
                },
                "content":{
                    "type":"text",
                    "analyzer":"my_analyzer",
                    "fielddata":True
                },
                "photo":{
                    "type":"keyword",
                },
                "price":{
                    "type":"integer",
                },
                "order":{
                    "type":"integer",
                },
                "score":{
                    "type":"float",
                },
                "is_active":{
                    "type":"keyword",
                },
                "created_at":{
                    "type":"date",
                },
            }
        }
        super().__init__(index_name=index_name)

    def create_index(self):
        settings = {
            "analysis": {
                "tokenizer": {
                    "kuromoji_search": {
                        "type": "kuromoji_tokenizer",
                        "mode" : "search",
                        "user_dictionary": "userdict_ja.txt"
                    }
                },
                "analyzer": {
                    "my_analyzer": {
                        "type": "custom",
                        "char_filter" : ["icu_normalizer", "kuromoji_iteration_mark"],
                        "tokenizer": "kuromoji_search",
                        "filter": ["kuromoji_baseform", "kuromoji_part_of_speech","kuromoji_stemmer","my_synonym_penguin_filter", "my_stop_filter"]
                    }
                },
                "filter":{
                    "my_synonym_penguin_filter": {
                        "type": "synonym",
                        "synonyms": ["コウテイペンギン,ペンギン"]
                    },
                    "my_stop_filter": {
                        "type": "stop",
                        "stopwords": ["いい", "もの", "ある", "いう", "それ", "いる"]
                    }
                }
            }
        }
        super().create_index(body={"settings":settings,"mappings":self.mappings})
        

    def insert_document(self,userkey,title,price,content='',photo='',id=None,):
        doc={
            'userkey':userkey,
            'title':title,
            'content':content,
            'photo':'/media/'+photo,
            'price':price,
            'order':0,
            'score':3.0,
            'is_active':'active',
            'created_at':datetime.now(),
        }
        super().insert_document(doc=doc,id=id,)


    #TODO 検索アルゴリズム書く
    def word_search(self,sort=created_at,word=""):
        query={
            "query": {
                "function_score": {
                    "query": { 
                        "bool":{
                            "should":{
                                "match":{
                                    "title":word
                                }
                            },
                            "filter":{
                                "term":{
                                    "is_active":"active"
                                }
                            }
                        },
                    },
                    "boost": "5",
                    "random_score": {}, 
                    "boost_mode": "multiply"
                }
            }
        }
      
        #sort=sort
        res = super().search(query=query)
        #print(res)
        return res["hits"]['hits']
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('args', help='args : string')
    args = parser.parse_args()

    commoditydoc = CommodityDoc()

    if args.args == 'delete_index':
        commoditydoc.delete_index()
        print('delete index')
    elif args.args == 'create_index':
        commoditydoc.create_index()
        print('create index')
    elif args.args == 'analyzer_check':
        commoditydoc.analyze_test("my_analyzer","猫に小判")

