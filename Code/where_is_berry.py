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
        x0 = np.array([[0.4],[0]])#np.zeros((n*2,1))
        P0 = np.diag([100]*(2*n))#np.zeros((2*n,2*n))
        self.kalman = kalman.Kalman(x0, P0)
        self.estimates_history = [[] for i in range(0,(len(self.anchors)))]   #inizialization as list of empty lists (as many lists as the number of anchors)
        self.last_times = np.zeros((n,1))
        self.last_time = None
        #udp
        self.dao = DAO.UDP_DAO("localhost", 12346) #Receive data (from nodered)
        self.data_interval = 0 #1000
        self.min_diff_anchors_ratio = 0.75
        self.min_diff_anchors = 1 #math.ceil(len(self.anchors)*self.min_diff_anchors_ratio)
        self.min_diff_anchors = 0 #math.ceil(len(self.anchors)*self.min_diff_anchors_ratio)
        self.alpha = 1.9 #0.9722921
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
            index = self.anchors_ids.index(self.get_id(m))
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
        measures = self.getMeasures()
        print 'minors:', [m['minor'] for m in measures]
        #print "Unfiltered:", measures
        #print "Batch:", len(measures)
        #meas = self.getMeasures()
        #measures = []
        #measures.append(self.getDistanceFromRSSI(meas))
        #measures.append(self.getDistanceFromFingerprinting(meas))

        unfiltered = measures
        for u in unfiltered:
            u['dist'] = round(10.0 ** (( self.TxPower - u['rssi'] )/(10.0 * self.alpha)), self.decimal_approximation)    #compute distance between device and anchor

        if filtered:
            print 'FILTRO'
            filtered_measures = {}

            n = len(self.anchors)
            batch_size = len(measures)

            ######F(k) - state transition model (static)
            now = time.time()
            if(self.last_time == None):
                self.last_time = now
            delta_t = [now - self.last_time]*(2*n)
            for m in measures:
                index = self.anchors_ids.index(self.get_id(m))
                #delta_t.append((m['timestamp'] - self.last_time[index][0])/1000)
            #print 'delta_t:', delta_t
            F = np.zeros((2*n,2*n))
            for i in range(1,2*n,2):
                F[i-1][i-1] = 1
                F[i-1][i] = delta_t[i]
                F[i][i] = 1
            print 'F', F

            ######H(k) - observation model (dynamic)
            H = np.zeros((batch_size,2*n))
            row_n = 0
            for m in measures:
                index = self.anchors_ids.index(self.get_id(m))
                H[row_n][(2*index)] = 1
                row_n += 1
            print 'H', H

            ######Q(k) - process noise covarinace matrix (static)
            Q = np.zeros((2*n,2*n))
            for i in range(1,2*n,2):
                Q[i-1][i-1] = 0.001
                #Q[i-1][i] = 0.001
                Q[i][i] = 0.001
            print 'Q', Q

            ######z(k) - measurement vector (dynamic)
            z = np.empty((batch_size,1))
            row_n = 0
            for m in measures:
                z[row_n] = m['rssi']
                row_n += 1
            print 'z', z

            ######R(k) - measurement noise matrix (dynamic)
            meas_noise_var = []
            for m in measures:
                _id = self.get_id(m)
                index = self.anchors_ids.index(_id)
                '''if len(self.estimates_history[index]) > 0:
                    var = np.var(np.array([self.estimates_history[index]]))
                else:
                    var = 1'''
                var = 100
                meas_noise_var.append(var)

            print 'var', meas_noise_var
            R = np.diag((meas_noise_var))
            print 'R', R

            #compute kalman filtering
            x = self.kalman.estimate(z, F, H, Q, R)
            print 'X FILTRATO\n', x

            #replace or append filtered measure to dictionary
            for m in measures:
                _id = self.get_id(m)
                index = self.anchors_ids.index(_id)
                print '********id:', _id, 'minor:', m['minor'], 'X:',x[index*2][0], 'rssi:', m['rssi']
                m['rssi'] = x[index*2][0]
                filtered_measures[_id] = m
            measures = [ filtered_measures[k] for k in filtered_measures ]
            print '++ measures', measures

            self.updateHistory(measures)
            #self.updateTimes(measures)
            self.last_time = now

        #print "Filtered:", measures
        distances = {}
        print "unfiltered"
        for u in unfiltered:
            print u['dist']
            distances['unfiltered'] = u['dist']
            print 'id:', u['minor'] , 'dist:', u['dist'], 'timestamp:', u['timestamp']

        print "filtered"
        for m in measures:
            dist = round(10.0 ** (( self.TxPower - m['rssi'] )/(10.0 * self.alpha)), self.decimal_approximation)    #compute distance between device and anchor
            m['dist'] = dist
            print dist
            distances['filtered'] = m['dist']
            print 'id:', m['minor'], 'dist:', m['dist'], 'timestamp:', m['timestamp']

        estimates = {}
        #estimates['timestamp'] = time.time() - self.start
        estimates['distances'] = distances

        message = {}
        message['measures'] = measures
        message['estimates'] = estimates
        #location = self.localization.trilateration(measures)
        #print 'BERRY E\' QUIIII!!!!!'
        #print location
        return message #location
