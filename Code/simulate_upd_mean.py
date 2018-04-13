"""
COMPUTE THE ERROR GIVEN BY WHERE_IS_BERRY
- launch WHERE_IS_BERRY
- send measure on UDP
- WHERE_IS_BERRY will read this the measure from UDP and return it back
- compare the result given by WHERE_IS_BERRY with the actual position
"""
from pymongo import MongoClient
import where_is_berry as wib
import DAO
import matplotlib.pyplot as plt
import pprint
import time
import numpy as np
import ast
import anchors_config as ac

#anchors
anc = ac.getAnchors()
anchors = anc['anchors']
anchors_ids = anc['anchors_ids']
anchor_id_keys = anc['idKeys']

# write actual coordinates on UDP_DAP
dao_coords = DAO.UDP_DAO("localhost", 12349)

# write on UDP to send to WHERE_IS_BERRY the test set
dao_test = DAO.UDP_DAO("localhost", 12348)

def split_id(_id): #TODO make it scalable
    i1 = _id.find(":")
    major = _id[:i1]
    i2 = _id.find(":", i1+1)
    uuid = _id[i1+1:i2]
    minor = _id[i2+1:]
    return [major, uuid, minor]

#get mongo collection
mongo = MongoClient()
db = mongo.fingerprinting   # db
test_map = db['test']    # 'test' collection

# for each position compute rssi averages
coords = test_map.find().distinct('coords')
last_time = 0
j = 0
while j < len(coords):
    c = coords[j]
    ts = time.time()
    if ts - last_time >= 0.5:
        dao_coords.writeData(c)
        data = {}
        i = 0
        while i < len(anchors_ids):
            a = anchors_ids[i]
            _id = split_id(a)
            major = _id[0]
            uuid = _id[1]
            minor = _id[2]
            timestamp = time.time()/1000
            data['major'] = major
            data['uuid'] = uuid
            data['minor'] = minor
            data['timestamp'] = timestamp
            # compute rssi avg
            tuples = list(test_map.find({'coords': {"y" : c['y'], "x" : c['x'], "z" : c['z']}, 'id': a}))
            rssis = [t['rssi'] for t in tuples]
            mean = np.mean(rssis)
            std = np.std(rssis)
            rssis = np.asarray(rssis)
            plt.hist(rssis)
            # remove outlier
            rssis = rssis[abs(rssis - mean) < 2 * std]
            mean = np.mean(rssis)
            print 'coords:', c
            print 'anchor:', a
            print 'mean:', np.mean(rssis)
            print 'var:', np.var(rssis)
            data['rssi'] = mean
            dao_test.writeData(data)
            i += 1
        j += 1
        last_time = ts
