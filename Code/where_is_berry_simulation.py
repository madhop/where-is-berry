import ast
import numpy as np
import time
import math
from decimal import Decimal
import random
import anchor as a
import anchors_config as ac
import trilateration
import fingerprinting
import kalman
import DAO
import ast
import measure
import time

class WhereIsBerry:
    def __init__(self, udp_port):
        self.trilateration = trilateration.Trilateration()
        self.fingerprinting = fingerprinting.Fingerprinting()
        self.start = time.time()
        #anchors
        anc = ac.getAnchors()
        self.anchors = anc['anchors']
        self.anchors_ids = anc['anchors_ids']
        self.anchor_id_keys = anc['idKeys']
        #kalman
        self.history_length = 100
        n = len(self.anchors)
        x0 = np.array([[-50], [0]]*n)#np.zeros((n*2,1))
        P0 = np.diag([20]*(2*n))#np.zeros((2*n,2*n))
        self.kalman = kalman.Kalman(x0, P0)
        self.estimates_history = [[] for i in range(0,(len(self.anchors)))]   #inizialization as list of empty lists (as many lists as the number of anchors)
        self.last_times = np.zeros((n,1))
        self.last_time = None
        #udp
        self.dao = DAO.UDP_DAO("localhost", udp_port) #Receive data (from nodered 12346, from simulation 12348)
        self.data_interval = -1000 #1000
        self.min_diff_anchors_ratio = 0.75
        self.min_diff_anchors = 8 #math.ceil(len(self.anchors)*self.min_diff_anchors_ratio)
        assert n >= self.min_diff_anchors, 'Not enough anchors: ' + str(n)
        # model
        self.alpha = 1.9 #0.9722921
        self.TxPower = -67.5
        self.decimal_approximation = 3

        self.batch_size = 1 #if 0: batch_size = len(measures) else batch_size = self.batch_size
        self.techniques = ['localization_trilateration_kalman',
                            'localization_trilateration_unfiltered',
                            'localization_fingerprinting_kalman',
                            'localization_fingerprinting_unfiltered']
        #self.techniques = ['localization_kalman', 'localization_unfiltered', 'localization_fingerprinting']


    def getData(self):
        return ast.literal_eval(self.dao.readData())

    #count how many different anchors have sent the signal
    def count_n_diff_anchors(self, measures_batch):
        diff_anchors = []
        for d in measures_batch:
            if d['id'] not in diff_anchors:
                diff_anchors.append(d['id'])
        return len(diff_anchors)

    #construct key
    def get_id(self, data):
        _id = ''
        for i in self.anchor_id_keys[:-1]:
            _id += str(data[i]) + ':'
        _id += str(data[self.anchor_id_keys[-1]])
        return _id

    def getMeasures(self):
        i = 0
        measures_batch = []
        data = self.getData()
        _id = self.get_id(data)
        i += 1
        print i, data
        if data['message'] == 0:
            return 0
        ts_milli = time.time() * 1000.0
        while not self.anchors.has_key(_id):    #go on only if the first is a good anchor
            ts_milli = time.time() * 1000.0
            data = self.getData()
            _id = self.get_id(data)
        #change id
        data['id'] = _id
        for k in self.anchor_id_keys:
            del data[k]
        measures_batch.append(data)
        while self.count_n_diff_anchors(measures_batch) < self.min_diff_anchors:
            data = self.getData()
            _id = self.get_id(data)
            i += 1
            print i, data
            if data['message'] == 0:
                return 0
            if self.anchors.has_key(_id):
                #change id
                data['id'] = _id
                for k in self.anchor_id_keys:
                    del data[k]
                measures_batch.append(data)
        #print 'measures_batch: ', measures_batch
        return measures_batch

    def updateHistory(self, measures):
        #for each of them update the history of etimated distances
        for m in measures:
            index = self.anchors_ids.index(m['id'])
            self.estimates_history[index].append(m['rssi'])
            #if there are enough value, remove oldest
            if len(self.estimates_history[index]) > self.history_length:
                self.estimates_history[index].pop(0)

    #compute distance between device and anchor
    def computeDist(self, rssi):
        return round(10.0 ** (( self.TxPower - rssi )/(10.0 * self.alpha)), self.decimal_approximation)


    def historyMean(self):
        means = [(sum(i)/len(i) if len(i) != 0 else 0) for i in self.estimates_history]
        return means

    def updateTimes(self, measures):
        for m in measures:
            index = self.anchors_ids.index(m['id'])
            self.last_times[index][0] = m['timestamp']

    def fingerprinting_measures(self, measurements):
        # for each anchor take only the last measure
        d = {}
        for un in measurements:
            d[un['id']] = un
        #measures = [d[l] for l in d]
        measures = []
        measures.append(d['1:b9407f30f5f8466eaff925556b57fe6d:1'])
        measures.append(d['1:b9407f30f5f8466eaff925556b57fe6d:2'])
        measures.append(d['1:b9407f30f5f8466eaff925556b57fe6d:5'])
        measures.append(d['1:b9407f30f5f8466eaff925556b57fe6d:7'])
        measures.append(d['1:b9407f30f5f8466eaff925556b57fe6d:4'])
        measures.append(d['1:b9407f30f5f8466eaff925556b57fe6d:8'])
        measures.append(d['1:b9407f30f5f8466eaff925556b57fe6d:9'])
        measures.append(d['1:b9407f30f5f8466eaff925556b57fe6d:10'])
        return measures

    def whereIsBerry(self, filtered):
        unfiltered = self.getMeasures()
        if unfiltered == 0:
            message = {'message' : 0}
            return message

        filtered_measures = []
        print 'FILTRO'
        meas_batch = min(self.batch_size, len(unfiltered))
        if self.batch_size == 0:
            meas_batch = len(unfiltered)

        for j in range(0,len(unfiltered), meas_batch):
            batch = []
            batch.append(unfiltered[j:j+meas_batch])
            for unfiltered_batch in batch:
                #print unfiltered_batch
                n = len(self.anchors)
                batch_size = len(unfiltered_batch)

                ######F(k) - state transition model (static)
                now = unfiltered_batch[-1]['timestamp']# np.mean([m['timestamp'] for m in measures])
                if(self.last_time == None):
                    self.last_time = now

                delta_t = (now - self.last_time)/1000.0
                delta_t_list = [delta_t]*(2*n)
                #print 'now', now
                #print 'self.last_time', self.last_time
                #print 'delta_t', delta_t
                F = np.zeros((2*n,2*n))
                for i in range(1,2*n,2):
                    F[i-1][i-1] = 1
                    F[i-1][i] = delta_t_list[i]
                    F[i][i] = 1
                #print 'F', F

                ######Q(k) - process noise covarinace matrix (static)
                phi = 0.001
                Q = np.zeros((2*n,2*n))
                for i in range(1,2*n,2):
                    Q[i-1][i-1] = (delta_t ** 3)/3
                    Q[i-1][i] = (delta_t ** 2)/2
                    Q[i][i-1] = (delta_t ** 2)/2
                    Q[i][i] = delta_t
                Q = Q * phi
                #print 'Q', Q

                ######z(k) - measurement vector (dynamic)
                z = np.empty((batch_size,1))
                ######R(k) - measurement noise matrix (dynamic)
                meas_noise_var = []
                ######H(k) - observation model (dynamic)
                H = np.zeros((batch_size,2*n))
                row_n = 0
                for m in unfiltered_batch:
                    index = self.anchors_ids.index(m['id'])
                    ##z
                    z[row_n][0] = m['rssi']
                    ##R
                    var = 60
                    meas_noise_var.append(var)
                    #H
                    H[row_n][(2*index)] = 1
                    row_n += 1

                #print 'var', meas_noise_var
                R = np.diag((meas_noise_var))
                #print 'R\n', R
                #print 'H\n', H
                #print 'z\n', z

                #compute kalman filtering
                x = self.kalman.estimate(z, F, H, Q, R)
                #print 'X FILTRATO\n', x
                #transform Kalman state in measures
                for state in range(0,len(x), 2):
                    m = {}
                    m['id'] = self.anchors_ids[state/2]
                    m['rssi'] = x[state][0]
                    m['timestamp'] = now
                    filtered_measures.append(m)
            self.last_time = now
            #END KALMAN FILTERING

        localizations = {}
        for t in self.techniques:
            '''
            TECHNIQUES:
            ['localization_trilateration_kalman',
            'localization_trilateration_unfiltered',
            'localization_fingerprinting_kalman',
            'localization_fingerprinting_unfiltered']
            '''
            if t == 'localization_trilateration_kalman':
                measures = filtered_measures
            elif t == 'localization_trilateration_unfiltered':
                measures = unfiltered
            elif t == 'localization_fingerprinting_kalman':
                measures = self.fingerprinting_measures(filtered_measures)
            elif t == 'localization_fingerprinting_unfiltered':
                measures = self.fingerprinting_measures(unfiltered)

            #COMMON PART FOR ALL TECHNIQUES
            message_measures = []
            for m in measures:
                _id = m['id']
                measure = {}
                measure['id'] = _id
                measure['rssi'] = m['rssi']
                measure['coordinates'] = self.anchors[_id].coordinates
                measure['timestamp'] = m['timestamp']    # millis
                measure['elapsed_time'] = m['timestamp']/1000.0 - self.start # sec
                measure['dist'] = self.computeDist(m['rssi'])
                message_measures.append(measure)
            # END COMMON PART

            if t == 'localization_trilateration_kalman':
                location = self.trilateration.trilateration(message_measures)
            elif t == 'localization_trilateration_unfiltered':
                location = self.trilateration.trilateration(message_measures)
            elif t == 'localization_fingerprinting_kalman':
                location = self.fingerprinting.knn(message_measures)
            elif t == 'localization_fingerprinting_unfiltered':
                location = self.fingerprinting.knn(message_measures)

            localization = {}
            #localization['measures'] = message_measures
            localization['location'] = location
            localizations[t] = localization
            # END FOR CYCLE ON TECHNIQUES
        message = {}
        #message['unfiltered_measures'] = unfiltered
        message['localizations'] = localizations
        message['timestamp'] = time.time()
        message['measures'] = unfiltered
        message['message'] = 1
        print 'BERRY E\' QUIIII!!!!!'
        return message
