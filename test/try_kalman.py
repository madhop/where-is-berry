import numpy as np
import time
import math
from decimal import Decimal
import random
import kalman


n = 5
x0 = np.zeros((n*2,1))
P0 = np.ones((2*n,2*n))#np.diag([1]*(2*n))
kalman = kalman.Kalman(x0, P0)
estimates_history = [[] for i in range(0,n)]   #inizialization as list of empty lists (as many lists as the number of anchors)
last_times = np.zeros((n,1))
last_time = None
history_length = 10

def updateHistory(measures):
    #for each of them update the history of etimated distances
    for m in measures:
        estimates_history[m['id']].append(m['rssi'])
        #if there are enough value, remove oldest
        if len(estimates_history[m['id']]) > history_length:
            estimates_history[m['id']].pop(0)

def historyMean():
        means = [(sum(i)/len(i) if len(i) != 0 else 0) for i in estimates_history]
        return means


count = 0
while count < 10:
    now = time.time()
    if(last_time == None):
        last_time = now
    if now - last_time >= 20:
        measures = []
        for i in range(0,n):
            measures.append({'id' : i, 'rssi' : random.random()})

        filtered_measures = {}

        ######F(k) - state transition model (static)
        delta_t = [now - last_time]*(2*n)
        print 'delta_t:', delta_t
        F = np.zeros((2*n,2*n))
        for i in range(1,2*n,2):
            F[i-1][i-1] = 1
            F[i-1][i] = delta_t[i]
            F[i][i] = 1
        print 'F', F

        ######H(k) - observation model (dynamic)
        H = np.zeros((n,2*n))
        for m in measures:
            H[m['id']][(2*m['id'])] = 1
        print 'H', H

        ######Q(k) - process noise covarinace matrix (static)
        Q = np.zeros((2*n,2*n))
        for i in range(1,2*n,2):
            Q[i-1][i-1] = 1
            Q[i-1][i] = 1
            Q[i][i] = 1
        print 'Q', Q

        ######z(k) - measurement vector (dynamic)
        z = np.empty((n,1))
        for m in measures:
            z[m['id']] = m['rssi']
        print 'z', z

        ######R(k) - measurement noise matrix (dynamic)
        delta_d_times_G = []
        G = 100 ######gain
        for m in measures:
            #delta_d_times_G.append((z[m['id']][0] -  historyMean()[m['id']])*G)
            delta_d_times_G.append(0.2)
        print 'delta_d * G', delta_d_times_G
        R = np.diag((delta_d_times_G))
        print 'R', R

        #compute kalman filtering
        x = kalman.estimate(z, F, H, Q, G, R)
        #print 'X FILTRATO', x

        #replace or append filtered measure to dictionary
        for m in measures:
            m['rssi'] = x[m['id']*2][0]
            filtered_measures[m['id']] = m

        filtered_measures = [ filtered_measures[k] for k in filtered_measures ]

        print filtered_measures
        print "history", estimates_history
        updateHistory(filtered_measures)
        last_time = now
        #count += 1
print "history", estimates_history
