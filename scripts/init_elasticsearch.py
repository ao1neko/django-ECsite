import subprocess
from ecsitecore.models import Commodity 
from ecsitecore.elasticsearch.commoditydoc import CommodityDoc
from ecsitecore.elasticsearch.db_functions import  convert_dbto_elastic


def run():
    commoditydoc = CommodityDoc()
    if commoditydoc.exist_index():
        commoditydoc.delete_index()
    commoditydoc.create_index()
    print("remake index")
    #forenkeyは使えない
    model_list=(Commodity,['id','title','content','photo','price',"order",'is_active','created_at','updated_at'])
    commoditydoc.set_mapping(model_list=model_list)
    print("change mapping")
    
    for ci in Commodity.objects.all():
        myjson=convert_dbto_elastic(Commodity,ci,model_list[1])
        commoditydoc.insert_document(doc=myjson,id=ci.pk,)
