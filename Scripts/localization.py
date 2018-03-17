import udpy
import ast
import numpy as np
import time
import math
from decimal import Decimal
import random
import beacon as b
import beacons_config as bc

class Localization:
    def __init__(self):
        self.udp_address = '127.0.0.1'
        self.udp_port = 12346
        self.data_interval = 1000
        self.min_diff_anchors_ratio = 0.75
        self.alpha = 0.9722921
        self.TxPower = -66.42379
        self.udp_dao = udpy.UDP_DAO(self.udp_address, self.udp_port)
        self.beacons = bc.estimotes()
        self.min_diff_anchors = math.ceil(len(self.beacons)*self.min_diff_anchors_ratio)
        self.decimal_approximation = 3


    #count how many different beacons have sent the signal
    def count_n_diff_anchors(self, measures_batch):
        diff_anchors = []
        for d in measures_batch:
            if d['minor'] not in diff_anchors:
                diff_anchors.append(d['minor'])
        return len(diff_anchors)

    def getData(self):
        return ast.literal_eval(self.udp_dao.readData())

    #construct key
    def get_id(self, beacon):
        return beacon['uuid'] + ':' + str(beacon['major']) + ':' + str(beacon['minor'])

    #Trilateration
    def trilateration(self, data):
        #print 'TRILATERATION'
        A = np.empty((0,2), dtype=float)
        b = np.empty((0,1), dtype=float)
        _id = self.get_id(data[-1])      #get _id of the last measure
        last_anchor = self.beacons[_id]  #get last anchor
        last_dist = data[-1]['dist']
        for d in data[:-1]:
            _id = self.get_id(d)
            anchor = self.beacons[_id] #get anchor
            A = np.append(A, [[ (last_anchor.x - anchor.x) , (last_anchor.y - anchor.y) ]], axis = 0)
            b_i = ((d['dist'] ** 2) - (last_dist ** 2)) - ((anchor.x ** 2) - (last_anchor.x **2)) - ((anchor.y ** 2) - (last_anchor.y **2))
            b = np.append(b, [[b_i]], axis=0)

        ls = np.linalg.lstsq(2*A,b, rcond=None)
        pos = {'x': ls[0][0][0], 'y' : ls[0][1][0], 'z':0 }
        return pos

    def getLocation(self):
        measures_batch = []
        ts_milli = time.time() * 1000
        data = self.getData()
        _id = self.get_id(data)
        while not self.beacons.has_key(_id):
            ts_milli = time.time() * 1000
            data = self.getData()
            _id = self.get_id(data)
        dist = round(10.0 ** (( self.TxPower - data['rssi'] )/(10.0 * self.alpha)), self.decimal_approximation)    #compute distance between device and beacon
        data['dist'] = dist #add to the data dictionary the distance
        meas = b.Measure(data['rssi'], dist, data['timestamp'])
        self.beacons[_id].measures.append(meas)  #store measurement in the beacon class
        measures_batch.append(data)
        while (data['timestamp'] - ts_milli) < self.data_interval or self.count_n_diff_anchors(measures_batch) < self.min_diff_anchors:
            data = self.getData()
            _id = self.get_id(data)
            if self.beacons.has_key(_id):
                dist = round(10.0 ** (( self.TxPower - data['rssi'] )/(10.0 * self.alpha)), self.decimal_approximation)    #compute distance between device and beacon
                data['dist'] = dist #add to the data dictionary the distance
                meas = b.Measure(data['rssi'], dist, data['timestamp'])
                self.beacons[_id].measures.append(meas)  #store measurement in the beacon class
                measures_batch.append(data)
        print 'measures_batch: ', len(measures_batch)
        location = self.trilateration(measures_batch)
        #location = {'x' : random.uniform(0.0, 5.0), 'y' : random.uniform(0.0, 5.0), 'z' : random.uniform(0.0, 5.0)}
        return location
