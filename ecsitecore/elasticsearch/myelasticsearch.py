from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import sys

class MyElasticSearch():
    def __init__(self,index_name="test"):
        self.index_name=index_name
        self.es = Elasticsearch()

    def create_index(self,body={"settings":{},"mappings":{}}):
        self.es.indices.create(index=self.index_name, body=body)

    def set_mapping(self,mappings):
        self.es.indices.close(index=self.index_name)
        self.es.indices.put_mapping(index=self.index_name, body=mappings)
        self.es.indices.open(index=self.index_name)
        

    def delete_index(self):
        self.es.indices.delete(index=self.index_name)
        
    def exist_index(self):
        res = self.es.indices.exists(index=self.index_name)
        return res #bool値
    
    def delete_document(self,id=1):
        res = self.es.delete(index=self.index_name, id=id)
        print(res['result'])


    def insert_document(self,doc,id=None):
        res = self.es.index(index=self.index_name,body=doc,id=id)
        print(res['result'])

    def search(self,query={"query": {"match_all": {}}}):
        return self.es.search(index=self.index_name, body=query)
        #print(res['hits']['total'])#ヒット数
        

    def show_indexies(self):
        res=self.es.indices.get_alias()
        print(res)

    def analyze_test(self,analyzer,text):
        res=self.es.indices.analyze(body={"analyzer": analyzer,"text": text},index=self.index_name)
        print(res)


    #bulk
    def bulk_sub_method(self,bulk_list):
        for bulk in bulk_list:
            yield {
                "_op_type": bulk["type"],
                "_index": bulk["index_name"],
                "_id": bulk["id"],
                "doc": bulk["doc"],
            }
    def bulk(self,bulk_list):
        helpers.bulk(self.es,self.bulk_sub_method(bulk_list))
        
if __name__ == '__main__':
    es=MyElasticSearch()
    es.show_indexies()
    
