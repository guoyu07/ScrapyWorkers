# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pymongo.operations import *
from pymongo import ASCENDING
from pymongo import DESCENDING
import random
import itertools


class PyMongoClient(object):


    def __init__(self, ip, port, user = None, pwd = None, **kwargs):
        if user is None or pwd == None:
            self.connect_string = "mongodb://%(ip)s:%(port)s/" % {
                "ip": ip,
                "port": port,
            }
        else:
            self.connect_string = "mongodb://%(user)s:%(pwd)s@%(ip)s:%(port)s/" % {
                "user": user,
                "pwd": pwd,
                "ip": ip,
                "port": port,
            }

        self.client = MongoClient(self.connect_string,
                           document_class=dict,
                           tz_aware=False,
                           connect=True,
                           maxPoolSize=kwargs.get("maxPoolSize", 10),
                           socketTimeoutMS=kwargs.get("socketTimeoutMS", 500000),
                           connectTimeoutMS=kwargs.get("connectTimeoutMS", 20000),
                           serverSelectionTimeoutMS=kwargs.get("serverSelectionTimeoutMS", 300000),
                           waitQueueTimeoutMS=kwargs.get("waitQueueTimeoutMS", 10000),
                           waitQueueMultiple=kwargs.get("waitQueueMultiple", 2),
                           socketKeepAlive=kwargs.get("socketKeepAlive", True)
                           )

    def remove(self, dbname, tablename, remove_dict):
        self.client[dbname][tablename].remove(remove_dict)  # 删除

    def bulkWrite(self, dbName, collectionName, requests):
        step = 300
        collect = self.client[dbName][collectionName]
        num = len(requests)
        for part, index in zip(itertools.count(0), range(0, num, step)):
            part_x = requests[part*step: (part+1)*step]
            try:
                collect.bulk_write(part_x)
            except:
                return requests[part*step:]
        return

    def database_names(self):
        return self.client.database_names()

    def collection_names(self, tablename):
        return self.client[tablename].collection_names(include_system_collections=False)

if __name__ == "__main__":

    pmc = PyMongoClient()
    # pmc.dropIndex("biqu", "UserEvent", [("partition_date", -1)])
    # for item in pmc.findElemIn("jh", "UserIP", "_id", ["221.232.131.162"], {"city": {"$exists": True}}, {"_id": False}):
    #     print item
    # data = {
    #     "key1": {"values": ["sssss"]},
    #     "key2": {"values": [None, None]}
    #         }
    client = pmc.getConn()
    print(client.database_names())
    # print(pmc.collection_names("biqu"))
    # db.collection_names(include_system_collections=False)
    # a = pmc.storeDaily(data, "hbtv", "test", {})
    # try:
    #     print("dddd", type(a), next(a))
    # except StopIteration:
    #     print("ssssss")




