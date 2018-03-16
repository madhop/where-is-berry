import udpy
import ast
import numpy as np
import time
import math
from decimal import Decimal
import beacon as b
import beacons_config as bc
print 'LOCALIZATION'


udp_dao = udpy.UDP_DAO('127.0.0.1', 12346)
uuid = "b9407f30f5f8466eaff925556b57fe6d"
data_interval = 1000
min_diff_anchors_ratio = 0.75
alpha = 0.9722921
TxPower = -66.42379
decimal_approximation = 3

beacons = bc.estimotes()#beacons, minors_list = bc.estimotes()
min_diff_anchors = math.ceil(len(beacons)*min_diff_anchors_ratio)


#count how many different beacons have sent the signal
def count_n_diff_anchors(measures_batch):
    diff_anchors = []
    for d in measures_batch:
        if d['minor'] not in diff_anchors:
            diff_anchors.append(d['minor'])
    return len(diff_anchors)


#construct key
def get_id(beacon):
    return beacon['uuid'] + ':' + str(beacon['major']) + ':' + str(beacon['minor'])

#Trilateration
def trilateration(data):
    print 'TRILATERATION'
    A = np.empty((0,2))
    b = np.empty((0,1))
    _id = get_id(data[-1])      #get _id of the last measure
    last_anchor = beacons[_id]  #get last anchor
    last_dist = data[-1]['dist']
    for d in data[:-1]:
        _id = get_id(d)
        anchor = beacons[_id] #get anchor
        A = np.append(A, [[ (last_anchor.x - anchor.x) , (last_anchor.y - anchor.y) ]], axis = 0)
        b_i = ((d['dist'] ** 2) - (last_dist ** 2)) - ((anchor.x ** 2) - (last_anchor.x **2)) - ((anchor.y ** 2) - (last_anchor.y **2))
        b = np.append(b, [[b_i]], axis=0)

    ls = np.linalg.lstsq(2*A,b, rcond=None)
    pos = ls[0]
    print pos
    print 'END TRILATERATION'
    return A


avg_time = 0
while True:
    measures_batch = []
    ts_milli = time.time() * 1000
    data = ast.literal_eval(udp_dao.readData())
    _id = get_id(data)
    if beacons.has_key(_id):
        print str(_id)
        dist = round(10.0 ** (( TxPower - data['rssi'] )/(10.0 * alpha)), decimal_approximation)    #compute distance between device and beacon
        data['dist'] = dist #add to the data dictionary the distance
        meas = b.Measure(data['rssi'], dist, data['timestamp'])
        beacons[_id].measures.append(meas)  #store measurement in the beacon class
        measures_batch.append(data)
        #print  'minor: ', beacons[_id].minor, 'dist: ', beacons[_id].measures[-1].distance, '#measures: ', len(beacons[_id].measures)
        while (data['timestamp'] - ts_milli) < data_interval or count_n_diff_anchors(measures_batch) < min_diff_anchors:
            data = ast.literal_eval(udp_dao.readData())
            _id = get_id(data)
            if beacons.has_key(_id):
                print str(_id)
                dist = round(10.0 ** (( TxPower - data['rssi'] )/(10.0 * alpha)), decimal_approximation)    #compute distance between device and beacon
                data['dist'] = dist #add to the data dictionary the distance
                meas = b.Measure(data['rssi'], dist, data['timestamp'])
                beacons[_id].measures.append(meas)  #store measurement in the beacon class
                measures_batch.append(data)
                #print 'measures_batch[-1][dist]: ', measures_batch[-1]['dist'], 'minor', measures_batch[-1]['minor']
        print 'measures_batch length: ', len(measures_batch)
        end_time = time.time() * 1000
        trilateration(measures_batch)
