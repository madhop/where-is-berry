from pymongo import MongoClient
import where_is_berry as wib
import DAO
import matplotlib.pyplot as plt
import pprint
import time
import numpy as np
import ast
import anchors_config as ac

test_map_name = 'test_30_random'#'test'

#anchors
anc = ac.getAnchors()
anchors = anc['anchors']
anchors_ids = anc['anchors_ids']
anchor_id_keys = anc['idKeys']

# write actual coordinates on UDP_DAO
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
test_map = db[test_map_name]    # 'test' collection

# for each position send rssi to WHERE_IS_BERRY
# Kalman / Fingerprinting
coords = test_map.find().distinct('coords')
last_time = 0
j = 0
while j < len(coords):
    print '################################\n################################\n################################\n################################'
    c = coords[j]
    c['message'] = 1
    print c
    ts = time.time()
    if ts - last_time >= 0.5:
        tuples = list(test_map.find({'coords': {"y" : c['y'], "x" : c['x'], "z" : c['z']}}))
        data = {}
        i = 0
        last_time2 = 0
        while i < len(tuples):
            ts2 = time.time()
            if ts2 - last_time2 >= 0.1:
                dao_coords.writeData(c)
                time.sleep(0.1)
                _id = split_id(tuples[i]['id'])
                major = _id[0]
                uuid = _id[1]
                minor = _id[2]
                timestamp = time.time()/1000
                data['major'] = major
                data['uuid'] = uuid
                data['minor'] = minor
                data['timestamp'] = timestamp
                rssi = tuples[i]['rssi']
                data['rssi'] = rssi
                data['message'] = 1
                #if it is the last measure of the last coordinate, send 0 as message
                if  i == len(tuples)-3 and j == len(coords)-1: #i == 23 and j == 1:
                    data['message'] = 0
                print 'i', i, 'j', j, data
                last_time2 = ts2
                dao_test.writeData(data)
                i += 1
        #dao_coords.writeData(c)
        j += 1
        last_time = ts


'''
# for each position compute rssi averages
# unfiltered
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
'''
