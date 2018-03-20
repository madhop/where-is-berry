import ast
import numpy as np
import time
import math
from decimal import Decimal
import random
import anchor as a
import anchors_config as ac
import localization
import kalman
import DAO
import ast
import measure


class WhereIsBerry:
    def __init__(self):
        self.localization = localization.Localization()
        #anchors
        anc = ac.getAnchors()
        self.anchors = anc['anchors']
        self.anchors_ids = anc['anchors_ids']
        self.anchor_id_keys = anc['idKeys']
        #kalman
        self.history_length = 5
        n = len(self.anchors)
        x0 = np.zeros((n*2,1))
        P0 = np.ones((2*n,2*n))#np.diag([1]*(2*n))
        self.kalman = kalman.Kalman(x0, P0, self.history_length)
        #udp
        self.dao = DAO.UDP_DAO("localhost", 12346)
        self.data_interval = 0 #1000
        self.min_diff_anchors_ratio = 0.75
        self.min_diff_anchors = 4#math.ceil(len(self.anchors)*self.min_diff_anchors_ratio)
        self.alpha = 0.9722921
        self.TxPower = -66.42379
        self.decimal_approximation = 3
        #batch of measures
        self.dist_history = []


    def getData(self):
        return ast.literal_eval(self.dao.readData())

    #count how many different anchors have sent the signal
    def count_n_diff_anchors(self, measures_batch):
        diff_anchors = []
        for d in measures_batch:
            if d['minor'] not in diff_anchors:
                diff_anchors.append(d['minor'])
        return len(diff_anchors)

    #construct key
    def get_id(self, data):
        _id = ''
        for i in self.anchor_id_keys[:-1]:
            _id += str(data[i]) + ':'
        _id += str(data[self.anchor_id_keys[-1]])
        return _id

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
        measures_batch.append(data)
        while (data['timestamp'] - ts_milli) < self.data_interval or self.count_n_diff_anchors(measures_batch) < self.min_diff_anchors:
            data = self.getData()
            _id = self.get_id(data)
            if self.anchors.has_key(_id):
                dist = round(10.0 ** (( self.TxPower - data['rssi'] )/(10.0 * self.alpha)), self.decimal_approximation)    #compute distance between device and anchor
                data['dist'] = dist #add to the data dictionary the distance
                measures_batch.append(data)
        print 'measures_batch: ', len(measures_batch)
        return measures_batch

    def whereIsBerry(self, filtered):
        measures = self.getMeasures()
        #meas = self.getMeasures()
        #measures = []
        #measures.append(self.getDistanceFromRSSI(meas))
        #measures.append(self.getDistanceFromFingerprinting(meas))


        if filtered:
            print 'FILTRO'
            filtered_measures = {}
            for m in measures:
                n = len(self.anchors)
                delta_t = [1]*(2*n)
                print 'delta_t:', delta_t
                #F(k) - state transition model
                F = np.zeros((2*n,2*n))
                for i in range(1,2*n,2):
                    F[i-1][i-1] = 1
                    F[i-1][i] = delta_t[i]
                    F[i][i] = 1
                print 'F', F

                #H(k) - observation model
                H = np.zeros((1,2*n))
                index = self.anchors_ids.index(self.get_id(m))
                H[0][(2*index)] = 1
                print 'H', H

                #Q(k) - process noise covarinace matrix
                Q = np.zeros((2*n,2*n))
                for i in range(1,2*n,2):
                    Q[i-1][i-1] = 1
                    Q[i-1][i] = 1
                    Q[i][i] = 1
                print 'Q', Q

                G = 100 #gain
                '''delta_d = np.zeros((n))
                z = np.zeros((n,1))
                z[index] = m['dist']
                delta_d = z - np.reshape(np.array([self.kalman.historyMean()]), (n,1))'''
                z = m['dist']
                delta_d = z - self.kalman.historyMean()[index]
                print 'delta_d', delta_d
                #R(k) - measurement noise matrix
                #R = np.diag((delta_d[:,0]*G).tolist())
                R = delta_d * G
                print 'R', R
                #compute kalman filtering
                x = self.kalman.estimate(z, F, H, Q, G, R)
                print 'X FILTRATO', x
                #replace or append filtered measure to dictionary
                _id = self.get_id(m)
                m['dist'] = x[index*2][0]
                filtered_measures[_id] = m
            measures = [ filtered_measures[k] for k in filtered_measures ]

        location = self.localization.trilateration(measures)
        print 'BERRY E\' QUIIII!!!!!'
        return location
