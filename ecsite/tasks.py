from __future__ import absolute_import, unicode_literals
from celery import shared_task

import time
from ecsitecore.elasticsearch.commoditydoc import CommodityDoc

commoditydoc = CommodityDoc()


@shared_task
def commodity_insert_document(userkey,title,content,photo,price):
    print("処理中")
    commoditydoc.insert_document(userkey=userkey,title=title,content=content,photo=photo,price=price)
    time.sleep(3)
    print("処理完了")

