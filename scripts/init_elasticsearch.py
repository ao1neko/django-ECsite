from ecsitecore.elasticsearch.commoditydoc import  CommodityDoc

def run():
    commoditydoc=CommodityDoc()
    if commoditydoc.exist_index():
        commoditydoc.delete_index()
        print("delete index")
    commoditydoc.create_index()
    print("set index")

