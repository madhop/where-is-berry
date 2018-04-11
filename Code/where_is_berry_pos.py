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
import time

class WhereIsBerry:
    def __init__(self):
        self.localization = localization.Localization()
        self.start = time.time()
        #anchors
        anc = ac.getAnchors()
        self.anchors = anc['anchors']
        self.anchors_ids = anc['anchors_ids']
        self.anchor_id_keys = anc['idKeys']
        #kalman
        self.history_length = 100
        n = 3 #x,y,z    #len(self.anchors)
        x0 = np.array([[0.5], [0]]*n)#np.zeros((n*2,1))
        P0 = np.diag([20]*(2*n))#np.zeros((2*n,2*n))
        self.kalman = kalman.Kalman(x0, P0)
        self.estimates_history = [[] for i in range(0,(len(self.anchors)))]   #inizialization as list of empty lists (as many lists as the number of anchors)
        self.last_times = np.zeros((n,1))
        self.last_time = None
        #udp
        self.dao = DAO.UDP_DAO("localhost", 12348) #Receive data (from nodered)
        self.data_interval = 0 #1000
        self.min_diff_anchors_ratio = 0.75
        self.min_diff_anchors = 3 #math.ceil(len(self.anchors)*self.min_diff_anchors_ratio)
        self.alpha = 1.7 #1.9 #0.9722921
        self.TxPower = -72
        self.decimal_approximation = 3
        self.batch_size = 0 #if 0: batch_size = len(measures) else batch_size = self.batch_size
        self.techniques = ['localization_kalman', 'localization_unfiltered']


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
        measures_batch = []
        ts_milli = time.time() * 1000.0
        data = self.getData()
        _id = self.get_id(data)
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

    def whereIsBerry(self, filtered):
        unfiltered = self.getMeasures()
        print 'unfiltered', unfiltered

        localizations = {}
        for t in self.techniques:
            message_measures = []
            location = {}
            if t == 'localization_kalman':
                print 'FILTRO'
                meas_batch = min(self.batch_size, len(unfiltered))
                if self.batch_size == 0:
                    meas_batch = len(unfiltered)

                for j in range(0,len(unfiltered), meas_batch):
                    batch = []
                    batch.append(unfiltered[j:j+meas_batch])
                    for unfiltered_batch in batch:
                        print unfiltered_batch

                        for u in unfiltered:
                            _id = u['id']
                            measure = {}
                            measure['id'] = _id
                            measure['rssi'] = u['rssi']
                            measure['coordinates'] = self.anchors[_id].coordinates
                            measure['timestamp'] = u['timestamp']    # millis
                            measure['elapsed_time'] = u['timestamp']/1000.0 - self.start # sec
                            measure['dist'] = self.computeDist(u['rssi'])
                            message_measures.append(measure)

                        location_unfiltered = self.localization.trilateration(message_measures)
                        n = 3 #len(self.anchors)
                        batch_size = 3 #len(unfiltered_batch)

                        ######F(k) - state transition model (static)
                        now = unfiltered_batch[-1]['timestamp']# np.mean([m['timestamp'] for m in measures])
                        if(self.last_time == None):
                            self.last_time = now

                        delta_t = (now - self.last_time)/1000.0
                        delta_t_list = [delta_t]*(2*n)
                        print 'now', now
                        print 'self.last_time', self.last_time
                        print 'delta_t', delta_t
                        F = np.zeros((2*n,2*n))
                        for i in range(1,2*n,2):
                            F[i-1][i-1] = 1
                            F[i-1][i] = delta_t_list[i]
                            F[i][i] = 1
                        print 'F', F

                        ######Q(k) - process noise covarinace matrix (static)
                        phi = 0.01
                        Q = np.zeros((2*n,2*n))
                        for i in range(1,2*n,2):
                            Q[i-1][i-1] = (delta_t ** 3)/3
                            Q[i-1][i] = (delta_t ** 2)/2
                            Q[i][i-1] = (delta_t ** 2)/2
                            Q[i][i] = delta_t
                        Q = Q * phi
                        print 'Q', Q

                        ######z(k) - measurement vector (dynamic)
                        z = np.empty((batch_size,1))
                        ######R(k) - measurement noise matrix (dynamic)
                        meas_noise_var = []
                        ######H(k) - observation model (dynamic)
                        H = np.zeros((batch_size,2*n))
                        row_n = 0
                        coords = ['x','y','z']
                        for c in coords:
                            ##z
                            z[row_n][0] = location_unfiltered[c]
                            ##R
                            var = 1000
                            meas_noise_var.append(var)
                            #H
                            H[row_n][(2*row_n)] = 1
                            row_n += 1

                        print 'var', meas_noise_var
                        R = np.diag((meas_noise_var))
                        print 'R', R
                        print 'H', H
                        print 'z', z

                        #compute kalman filtering
                        x = self.kalman.estimate(z, F, H, Q, R)
                        print 'X FILTRATO\n', x
                        #transform Kalman state in measures
                        for i in range(0,len(x), 2):
                            location[coords[i/2]] = x[i][0]

                    #self.updateHistory(filtered_measures)
                    #self.updateTimes(measures)
                    self.last_time = now

            #END IF FILTERED
            elif t == 'localization_unfiltered':
                for u in unfiltered:
                    _id = u['id']
                    measure = {}
                    measure['id'] = _id
                    measure['rssi'] = u['rssi']
                    measure['coordinates'] = self.anchors[_id].coordinates
                    measure['timestamp'] = u['timestamp']    # millis
                    measure['elapsed_time'] = u['timestamp']/1000.0 - self.start # sec
                    measure['dist'] = self.computeDist(u['rssi'])
                    message_measures.append(measure)
                if self.min_diff_anchors >= 3:
                    location = self.localization.trilateration(message_measures)

            localization = {}
            localization['measures'] = message_measures
            localization['location'] = location
            localizations[t] = localization
            #END FOR T IN TECHNIQUES
        message = {}
        message['localizations'] = localizations
        message['timestamp'] = time.time()

        print 'BERRY E\' QUIIII!!!!!'
        return message
