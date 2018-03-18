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
        self.kalman = kalman.Kalman()
        self.dao = DAO.UDP_DAO("localhost", 12346)
        anc = ac.getAnchors()
        self.anchors = anc['anchors']
        self.anchors_ids = anc['anchors_ids']
        self.data_interval = 0 #1000
        self.min_diff_anchors_ratio = 0.75
        self.min_diff_anchors = 1#math.ceil(len(self.anchors)*self.min_diff_anchors_ratio)
        self.alpha = 0.9722921
        self.TxPower = -66.42379
        self.decimal_approximation = 3


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
        for i in self.anchors['idKeys'][:-1]:
            _id += str(data[i]) + ':'
        _id += str(data[self.anchors['idKeys'][-1]])
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

        if filtered:
            print 'FILTRO'
            n = len(self.anchors)
            x0 = np.zeros((n*2,1))
            P0 = np.diag(2*n)#np.zeros((2*n,2*n))
            kalman = kalman.Kalman(x0, P0)
            delta_t = []
            #F(k) - state transition model
            F = np.zeros((2*n,2*n))
            for i in range(1,2*n,2):
                F[i-1][i-1] = 1
                F[i-1][i] = delta_t
                F[i][i] = 1

            #H(k) - observation model
            #il batch deve essere 1, se non e' 1, bisogna decidere cosa fare (media, o solo il primo ecc.)
            H = np.zeros((n,2*n))
            index = self.anchors_ids.index(self.get_id(measures[0]))
            H[index][(2*index)] = 1

            #Q(k) - process noise covarinace matrix
            Q = np.zeros((2*n,2*n))
            for i in range(1,2*n,2):
                Q[i-1][i-1] = 1
                Q[i-1][i] = 1
                Q[i][i] = 1

            G = 100 #gain
            delta_d = np.zeros((n)) #d - history_mean_d
            #R(k) - measurement noise matrix
            R = np.zeros((n,n))
            for i in range(0,n):
                R[i][i] = delta_d[i] * G
            measures = kalman.estimate(measures, F, H, Q, G, R)

        location = self.localization.trilateration(measures)
        print 'BERRY E\' QUIIII!!!!!'
        return location
