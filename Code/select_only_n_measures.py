from pymongo import MongoClient
from bson.objectid import ObjectId
import time
import numpy as np
import ast
import random

# number of element that you want in the db
n = 150

#get mongo collection
mongo = MongoClient()
db = mongo.fingerprinting   # db
map = db['luca_01']    # 'test' collection


coords = map.find().distinct('coords')
anchors_ids = map.find().distinct('id') # db.luca_01.find().distinct('id')
print 'anchors_ids', len(anchors_ids)

iterations = 0
for j in range(0,len(coords)):
    c = coords[j]
    print '#####iterations', iterations
    iterations += 1
    print c
    data = {}
    for i in range(0,len(anchors_ids)):
        a = anchors_ids[i]
        tuples = map.find({'coords': {"y" : c['y'], "x" : c['x'], "z" : c['z']}, 'id': a})
        print 'prima- tuples', tuples.count()
        while tuples.count() > n:
            obj_ids = list(tuples.distinct('_id'))
            ranran = int(tuples.count() * random.random())
            print 'obj_id', obj_ids[ranran]
            map.remove({'_id' : ObjectId(str(obj_ids[ranran]))})
            tuples = map.find({'coords': {"y" : c['y'], "x" : c['x'], "z" : c['z']}, 'id': a})
            print 'dopo - tuples', tuples.count()
