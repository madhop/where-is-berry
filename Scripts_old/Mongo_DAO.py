import pymongo as pm

class Mongo_DAO:
    def __init__(address, port):
        self.mongo = pm.MongoClient(address,port)

    def __init__():
        self.mongo = pm.MongoClient()

    def readAllData(db, collection, condition = {}):
        db = self.mongo[db]
        collection = db[collection]
        data = list(collection.find(condition))
        return data

    def readBatchData(db, collection, condition = {}, batch):
        db = self.mongo[db]
        collection = db[collection]
        data = list(collection.find(condition).limit(batch))
        return data

    def readDistinct(db, collection, condition = {}, batch, dist_att):
        db = self.mongo[db]
        collection = db[collection]
        data = list(collection.find(condition).distinct(dist))
        return data
