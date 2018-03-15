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
'''
def count_n_diff_anchors(distances):
    minors = []
    for d in distances:
        if d.minor not in minors:
            minors.append(d.minor)
    return len(minors)
'''

#construct key
def get_id(beacon):
    return beacon['uuid'] + ':' + str(beacon['major']) + ':' + str(beacon['minor'])


avg_time = 0
while True:
    diff_available_anchors = []
    ts_milli = time.time() * 1000
    data = ast.literal_eval(udp_dao.readData())
    _id = get_id(data)
    if beacons.has_key(_id):
        print str(_id)
        dist = round(10.0 ** (( TxPower - data['rssi'] )/(10.0 * alpha)), decimal_approximation)
        meas = b.Measure(data['rssi'], dist, data['timestamp'])
        beacons[_id].measures.append(meas)
        diff_available_anchors.append(_id)
        print  'minor: ', beacons[_id].minor, 'dist: ', beacons[_id].measures[-1].distance, '#measures: ', len(beacons[_id].measures)
        while (data['timestamp'] - ts_milli) < data_interval or len(diff_available_anchors) < min_diff_anchors:
            data = ast.literal_eval(udp_dao.readData())
            _id = get_id(data)
            if beacons.has_key(get_id(data)):
                print str(_id)
                dist = round(10.0 ** (( TxPower - data['rssi'] )/(10.0 * alpha)), decimal_approximation)
                meas = b.Measure(data['rssi'], dist, data['timestamp'])
                beacons[_id].measures.append(meas)
                diff_available_anchors.append(_id)
                print  'minor: ', beacons[_id].minor, 'dist: ', beacons[_id].measures[-1].distance, '#measures: ', len(beacons[_id].measures)
        print 'diff_available_anchors: ', len(diff_available_anchors)
        end_time = time.time() * 1000
    #TODO ADD LOCALIZATION
    #remove all measurements for each beacon
    for _id in diff_available_anchors:
        beacons[_id].measures = []
