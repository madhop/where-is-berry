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
        n = len(self.anchors)
        x0 = np.array([[0.5], [0]]*n)#np.zeros((n*2,1))
        P0 = np.diag([20]*(2*n))#np.zeros((2*n,2*n))
        self.kalman = kalman.Kalman(x0, P0)
        self.estimates_history = [[] for i in range(0,(len(self.anchors)))]   #inizialization as list of empty lists (as many lists as the number of anchors)
        self.last_times = np.zeros((n,1))
        self.last_time = None
        #udp
        self.dao = DAO.UDP_DAO("localhost", 12346) #Receive data (from nodered)
        self.data_interval = 0 #1000
        self.min_diff_anchors_ratio = 0.75
        self.min_diff_anchors = 1 #math.ceil(len(self.anchors)*self.min_diff_anchors_ratio)
        self.alpha = 1.9 #0.9722921
        self.TxPower = -67.5
        self.decimal_approximation = 3
        self.batch_size = 0 #if 0: batch_size = len(measures) else batch_size = self.batch_size


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
        data['elapsed_time'] = data['timestamp']/1000 - self.start
        measures_batch.append(data)
        while (data['timestamp'] - ts_milli) < self.data_interval or self.count_n_diff_anchors(measures_batch) < self.min_diff_anchors:
            data = self.getData()
            _id = self.get_id(data)
            if self.anchors.has_key(_id):
                data['elapsed_time'] = data['timestamp']/1000 - self.start
                measures_batch.append(data)
        #print 'measures_batch: ', len(measures_batch)
        return measures_batch

    def updateHistory(self, measures):
        #for each of them update the history of etimated distances
        for m in measures:
            index = self.anchors_ids.index(m['id'])
            self.estimates_history[index].append(m['rssi'])
            #if there are enough value, remove oldest
            if len(self.estimates_history[index]) > self.history_length:
                self.estimates_history[index].pop(0)


    def historyMean(self):
        means = [(sum(i)/len(i) if len(i) != 0 else 0) for i in self.estimates_history]
        return means

    def updateTimes(self, measures):
        for m in measures:
            index = self.anchors_ids.index(self.get_id(m))
            self.last_times[index][0] = m['timestamp']

    def whereIsBerry(self, filtered):
        unfiltered = self.getMeasures()
        print 'minors:', [u['minor'] for u in unfiltered]

        message = {}

        for u in unfiltered:
            u['dist'] = round(10.0 ** (( self.TxPower - u['rssi'] )/(10.0 * self.alpha)), self.decimal_approximation)    #compute distance between device and anchor

        if filtered:
            print 'FILTRO'
            meas_batch = min(self.batch_size, len(unfiltered))
            if self.batch_size == 0:
                meas_batch = len(unfiltered)

            for j in range(0,len(unfiltered), meas_batch):
                batch = []
                batch.append(unfiltered[j:j+meas_batch])
                for unfiltered_batch in batch:

                    n = len(self.anchors)
                    batch_size = len(unfiltered_batch)

                    ######F(k) - state transition model (static)
                    now = unfiltered_batch[-1]['timestamp']# np.mean([m['timestamp'] for m in measures])
                    if(self.last_time == None):
                        self.last_time = now
                    delta_t = [(now - self.last_time)/1000]*(2*n)
                    print 'delta_t', delta_t
                    #print 'delta_t:', delta_t
                    F = np.zeros((2*n,2*n))
                    for i in range(1,2*n,2):
                        F[i-1][i-1] = 1
                        F[i-1][i] = delta_t[i]
                        F[i][i] = 1
                    print 'F', F


                    ######Q(k) - process noise covarinace matrix (static)
                    Q = np.zeros((2*n,2*n))
                    for i in range(1,2*n,2):
                        Q[i-1][i-1] = 0
                        #Q[i-1][i] = 0.001
                        Q[i][i] = 0
                    print 'Q', Q

                    ######z(k) - measurement vector (dynamic)
                    '''z = np.empty((batch_size,1))
                    row_n = 0
                    for m in unfiltered_batch:
                        z[row_n][0] = m['rssi']
                        row_n += 1
                    print 'z', z'''

                    ######H(k) - observation model (dynamic)
                    '''H = np.zeros((batch_size,2*n))
                    row_n = 0
                    for m in unfiltered_batch:
                        index = self.anchors_ids.index(self.get_id(m))
                        H[row_n][(2*index)] = 1
                        row_n += 1
                        print 'H', H'''

                    ######z(k) - measurement vector (dynamic)
                    z = np.empty((batch_size,1))
                    ######R(k) - measurement noise matrix (dynamic)
                    meas_noise_var = []
                    ######H(k) - observation model (dynamic)
                    H = np.zeros((batch_size,2*n))
                    row_n = 0
                    for m in unfiltered_batch:
                        index = self.anchors_ids.index(self.get_id(m))
                        ##z
                        z[row_n][0] = m['rssi']
                        ##R
                        '''if len(self.estimates_history[index]) > 0:
                            var = np.var(np.array([self.estimates_history[index]]))
                        else:
                            var = 1'''
                        var = 30
                        meas_noise_var.append(var)
                        #H
                        H[row_n][(2*index)] = 1
                        row_n += 1

                    print 'var', meas_noise_var
                    R = np.diag((meas_noise_var))
                    print 'R', R
                    print 'H', H
                    print 'z', z

                    #compute kalman filtering
                    x = self.kalman.estimate(z, F, H, Q, R)
                    print 'X FILTRATO\n', x

            filtered_measures = []
            for a in self.anchors:
                _id = self.anchors[a].getID()
                index = self.anchors_ids.index(_id)
                fm = {}
                fm['id'] = _id
                fm['rssi'] = x[index*2][0]
                fm['coordinates'] = self.anchors[a].coordinates
                fm['timestamp'] = now
                fm['elapsed_time'] = now - self.start
                dist = round(10.0 ** (( self.TxPower - fm['rssi'] )/(10.0 * self.alpha)), self.decimal_approximation)    #compute distance between device and anchor
                fm['dist'] = dist
                filtered_measures.append(fm)

            filtered_location = {}
            if len(self.anchors) > 3:
                filtered_location = self.localization.trilateration(filtered_measures)
            self.updateHistory(filtered_measures)
            #self.updateTimes(measures)
            self.last_time = now

            localization_kalman = {}
            localization_kalman['measures'] = filtered_measures
            localization_kalman['location'] = filtered_location
            message['localization_kalman'] = localization_kalman

        unfiltered_measures = []
        for u in unfiltered:
            _id = self.get_id(u)
            dist = round(10.0 ** (( self.TxPower - u['rssi'] )/(10.0 * self.alpha)), self.decimal_approximation)    #compute distance between device and anchor
            um = {}
            um['id'] = _id
            um['rssi'] = u['rssi']
            um['coordinates'] = self.anchors[_id].coordinates
            um['timestamp'] = u['timestamp']
            um['elapsed_time'] = u['timestamp'] - self.start
            um['dist'] = dist
            unfiltered_measures.append(um)

        unfiltered_location = {}
        if len(self.anchors) > 3:
            unfiltered_location = self.localization.trilateration(unfiltered_measures)

        localization_unfiltered = {}
        localization_unfiltered['measures'] = unfiltered_measures
        localization_unfiltered['location'] = unfiltered_location
        message['localization_unfiltered'] = localization_unfiltered

        print 'BERRY E\' QUIIII!!!!!'
        return message #location
