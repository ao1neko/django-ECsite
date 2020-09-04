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



    
    def __init__(self):
        self.mappings = {"properties": {}}
        super().__init__(index_name="commodity")

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
        

    def set_mapping(self,model_list=[]):
        model_class=model_list[0]
        model_fileds=model_list[1]
        myjson={}
        for model_filed in model_fileds:
            model_filed_class=model_class._meta.get_field(model_filed).__class__.__name__
            if model_filed_class == 'TextField' :
                tmp={}
                tmp['type']='text'
                tmp['analyzer']='my_analyzer'
                tmp['fielddata']=True
                myjson[str(model_filed)]=tmp
            elif model_filed_class == "CharField" :
                tmp={}
                tmp['type']='keyword'
                myjson[str(model_filed)]=tmp
            elif model_filed_class == 'ImageField' :
                tmp={}
                tmp['type']='text'
                myjson[str(model_filed)]=tmp
            elif model_filed_class == 'IntegerField':
                tmp={}
                tmp['type']='integer'
                myjson[str(model_filed)]=tmp
            elif model_filed_class == 'DateTimeField':
                tmp={}
                tmp['type']='date'
                myjson[str(model_filed)]=tmp
            elif model_filed_class != 'AutoField':
                print("フィールドタイプが適切ではありません",model_filed_class)
                sys.exit(1)
        self.mappings = {"properties": myjson}
        super().set_mapping(mappings = self.mappings)

    #TODO 引数後で追加,関数内部でdoc作成
    def insert_document(self,doc,id=None,):
        super().insert_document(doc=doc,id=id,)

    def search(self,sort=created_at):
        query={
            "query": {
                "bool":{
                    "filter":{
                        "term":{
                            "is_active":"active"
                        }
                    }
                }
            },
            "sort":sort
        }
        res = super().search(query=query)
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

