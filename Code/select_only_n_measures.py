from pymongo import MongoClient
from bson.objectid import ObjectId
import time
import numpy as np
import ast
import random

# number of element that you want in the db
n = 30  #150

#get mongo collection
mongo = MongoClient()
db = mongo.fingerprinting   # db
map = db['test']  # 'luca_01'  # 'test' collection
insert_map = db['test_30meas']
randomized_map = db['test_30_random']


coords = map.find().distinct('coords')
anchors_ids = map.find().distinct('id') # db.luca_01.find().distinct('id')
print 'anchors_ids', len(anchors_ids)


def create():
    iterations = 0
    # for each coordinate
    for j in range(0,len(coords)):
        c = coords[j]
        print '#####iteration', iterations
        iterations += 1
        print c
        data = {}
        # for each anchor
        for i in range(0,len(anchors_ids)):
            a = anchors_ids[i]
            tuples = np.asarray(list(map.find({'coords': {"y" : c['y'], "x" : c['x'], "z" : c['z']}, 'id': a})))
            print 'tuples', len(tuples)
            indices = []
            for i in range(n):
                index = int(len(tuples) * random.random())
                while index in indices:
                    index = int(len(tuples) * random.random())
                indices.append(index)
                del tuples[index]['_id']
                print(tuples[index])
                print i
            tuples = tuples[indices].tolist()
            print len(tuples)
            insert_map.insert(tuples)

            """
            # remove one at the time from an existing collection
            print 'prima - tuples', tuples.count()
            while tuples.count() > n:
                obj_ids = list(tuples.distinct('_id'))
                ranran = int(tuples.count() * random.random())
                print 'obj_id', obj_ids[ranran]
                map.remove({'_id' : ObjectId(str(obj_ids[ranran]))})
                tuples = map.find({'coords': {"y" : c['y'], "x" : c['x'], "z" : c['z']}, 'id': a})
                print 'dopo - tuples', tuples.count()"""

def make_random(input_map):
    randomized_tuples = []
    tuples = np.asarray(list(input_map.find()))
    tuples_indices = range(len(tuples))
    i = int(len(tuples_indices) * random.random())
    print 'at first the length is', len(tuples_indices)
    while len(tuples_indices) > 0:
        index = tuples_indices[i]
        print index
        del tuples_indices[i]
        i = int(len(tuples_indices) * random.random())
        t = tuples[index]
        del t['_id']
        randomized_tuples.append(t)
    print 'randomized_tuples', len(randomized_tuples)
    randomized_map.insert(randomized_tuples)


#create()
make_random(db['test_30meas'])
