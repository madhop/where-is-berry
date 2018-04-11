from pymongo import MongoClient
import socket
import DAO
import time

map_name = 'luca_01'

dao = DAO.UDP_DAO("localhost", 12348)

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

tuples = list(map.find({'coords': {"y" : 3.69, "x" : 0.74, "z" : 0.41}}))

last_time = time.time()
while True:
    for i in range(0,len(tuples)):
        data = {}
        ts = time.time()
        if ts - last_time >= 0.1:
            major, uuid, minor = split_id(tuples[i]['id'])
            timestamp = time.time()/1000#tuples[i]['timestamp']
            rssi = tuples[i]['rssi']
            data['major'] = major
            data['uuid'] = uuid
            data['minor'] = minor
            data['timestamp'] = timestamp
            data['rssi'] = rssi
            print data
            dao.writeData(data)
            last_time = ts
