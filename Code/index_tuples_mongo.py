from pymongo import MongoClient
import socket
import DAO
import time

map_name = 'luca_01_unindexed'

dao = DAO.UDP_DAO("localhost", 12346)

def split_id(_id): #TODO make it scalable
    i1 = _id.find(":")
    major = _id[:i1]
    i2 = _id.find(":", i1+1)
    uuid = _id[i1+1:i2]
    minor = _id[i2+1:]
    return major, uuid, minor

#get mongo collection
mongo = MongoClient()
db = mongo.fingerprinting   # db
map = db[map_name]    # collection
tuples = map.find()
coords = list(tuples.distinct("coords"))
i = 1
new_tuples = []
for c in coords:
    tuplesPerCoord = map.find({"coords" : {'x' : c['x'], 'y' : c['y'], 'z' : c['z']}})
    #tuplesPerCoord['index'] = i
    for t in tuplesPerCoord:
        t['index'] = i
        new_tuples.append(t)
    i+=1

print new_tuples

db['luca_01'].insert(new_tuples)
