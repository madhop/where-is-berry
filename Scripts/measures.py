import udpy
import ast
import numpy as np
import time
import math
from decimal import Decimal
import random
import anchor as a
import anchors_config as bc
import kalman

class MeasuresRetriever:
    def __init__(self):
        self.udp_address = '127.0.0.1'
        self.udp_port = 12346
        self.data_interval = 1000
        self.min_diff_anchors_ratio = 0.75
        self.alpha = 0.9722921
        self.TxPower = -66.42379
        self.udp_dao = udpy.UDP_DAO(self.udp_address, self.udp_port)
        self.anchors = bc.getAnchors()
        self.min_diff_anchors = math.ceil(len(self.anchors)*self.min_diff_anchors_ratio)
        self.decimal_approximation = 3


    #count how many different anchors have sent the signal
    def count_n_diff_anchors(self, measures_batch):
        diff_anchors = []
        for d in measures_batch:
            if d['minor'] not in diff_anchors:
                diff_anchors.append(d['minor'])
        return len(diff_anchors)

    def getData(self):
        return ast.literal_eval(self.udp_dao.readData())

    #construct key
    def get_id(self, data):
        _id = ''
        for i in self.anchors['idKeys'][:-1]:
            _id += str(data[i]) + ':'
        _id += str(data[self.anchors['idKeys'][-1]])
        return _id#data['uuid'] + ':' + str(data['major']) + ':' + str(data['minor'])

    def getMeasures(self):
        measures_batch = []
        ts_milli = time.time() * 1000
        data = self.getData()
        _id = self.get_id(data)
        while not self.anchors.has_key(_id):    #go on only if the first is a good anchor
            ts_milli = time.time() * 1000
            data = self.getData()
            _id = self.get_id(data)
        dist = round(10.0 ** (( self.TxPower - data['rssi'] )/(10.0 * self.alpha)), self.decimal_approximation)    #compute distance between device and anchor
        data['dist'] = dist #add to the data dictionary the distance
        meas = a.Measure(data['rssi'], dist, data['timestamp'])
        self.anchors[_id].measures.append(meas)  #store measurement in the anchor class
        measures_batch.append(data)
        while (data['timestamp'] - ts_milli) < self.data_interval or self.count_n_diff_anchors(measures_batch) < self.min_diff_anchors:
            data = self.getData()
            _id = self.get_id(data)
            if self.anchors.has_key(_id):
                dist = round(10.0 ** (( self.TxPower - data['rssi'] )/(10.0 * self.alpha)), self.decimal_approximation)    #compute distance between device and anchor
                data['dist'] = dist #add to the data dictionary the distance
                meas = a.Measure(data['rssi'], dist, data['timestamp'])
                self.anchors[_id].measures.append(meas)  #store measurement in the anchor class
                measures_batch.append(data)
        print 'measures_batch: ', len(measures_batch)
        return measures_batch
