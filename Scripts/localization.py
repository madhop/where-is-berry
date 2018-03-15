import udpy
import ast
import numpy as np
import time
import math
from decimal import Decimal

udp_dao = udpy.UDP_DAO('127.0.0.1', 12346)

beacon1 = np.array([0 , 0])

majors_avail = [1]
minors_avail = [4]#[1,2,3,4,5]
data_interval = 1000
n_diff_anchors_ratio = 0.75
alpha = 0.9722921
TxPower = -66.42379

n_diff_anchors = math.ceil(len(minors_avail)*n_diff_anchors_ratio)
print "n_diff_anchors: ", n_diff_anchors

def count_n_diff_anchors(distances):
    minors = []
    for d in distances:
        if d['minor'] not in minors:
            minors.append(d['minor'])
    return len(minors)


avg_time = 0
while True:
    distances = []
    ts_milli = time.time() * 1000
    data = ast.literal_eval(udp_dao.readData())
    if data['major'] in majors_avail and (data['minor'] in minors_avail):
        dist = round(10.0 ** (( TxPower - data['rssi'] )/(10.0 * alpha)), 2)
        data['dist'] = dist
        distances.append(data)
        while (data['timestamp'] - ts_milli) < data_interval or count_n_diff_anchors(distances) < n_diff_anchors:
            data = ast.literal_eval(udp_dao.readData())
            if data['major'] in majors_avail and (data['minor'] in minors_avail):
                dist = round(10.0 ** (( TxPower - data['rssi'] )/(10.0 * alpha)), 2)
                data['dist'] = dist
                distances.append(data)
                print  'minor: ' + str(data['minor']) + ' - rssi: ' + str(data['rssi']) + ' - time: ' + str(data['timestamp']) + ' - dist: ' + str(dist)
        print 'distances: ', len(distances)
        end_time = time.time() * 1000
