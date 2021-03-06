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

class Localization:
    def __init__(self):
        '''self.udp_address = '127.0.0.1'
        self.udp_port = 12346'''
        '''self.data_interval = 1000
        self.min_diff_anchors = math.ceil(len(self.anchors)*self.min_diff_anchors_ratio)
        self.min_diff_anchors_ratio = 0.75'''
        '''self.alpha = 0.9722921
        self.TxPower = -66.42379
        self.decimal_approximation = 3'''
        #self.udp_dao = udpy.UDP_DAO(self.udp_address, self.udp_port)
        #self.anchors = bc.getAnchors()


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

    #Trilateration
    def trilateration(self, data):
        #print 'TRILATERATION'
        _id = self.get_id(data[-1])      #get _id of the last measure
        last_anchor = self.anchors[_id]  #get last anchor
        last_dist = data[-1]['dist']
        A = np.empty((0,len(last_anchor.coordinates)), dtype=float)
        b = np.empty((0,1), dtype=float)
        for d in data[:-1]:
            _id = self.get_id(d)
            anchor = self.anchors[_id]  #get anchor
            A_row = []
            b_i = (d['dist'] ** 2)
            for c in anchor.coordinates.keys():
                A_row.append( last_anchor.coordinates[c] - anchor.coordinates[c] )
                b_i -= ((anchor.coordinates[c] ** 2) - (last_anchor.coordinates[c] **2))
            A = np.append(A, [A_row], axis = 0)
            b = np.append(b, [[b_i]], axis=0)

        ls = np.linalg.lstsq(2*A,b, rcond=None)
        pos = {}
        i = 0
        for c in anchor.coordinates.keys():
            pos[c] = ls[0][i][0]
            i += 1
        print pos
        return pos

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
        location = self.trilateration(measures_batch)
        #location = {'x' : random.uniform(0.0, 5.0), 'y' : random.uniform(0.0, 5.0), 'z' : random.uniform(0.0, 5.0)}
        return location

        def getLocation(self, filtered = True):
            measures = self.getMeasures()
            if filtered:
                x0 =
                P0 =
                kalman = kalman.Kalman(x0, P0)
                delta_t = []
                #F(k) - state transition model
                F = np.zeros((2*n,2*n))
                for i in range(1,2*n,2):
                    F[i-1][i-1] = 1
                    F[i-1][i] = delta_t
                    F[i][i] = 1
                measures = kalman.estimate(measures, F, H, Q, G, R)

            location = self.trilateration(measures)
            return location
