import udpy
import ast
import numpy as np
import time
import math
from decimal import Decimal
import random

class Localization:
    def __init__(self):
        self.udp_address = '127.0.0.1'
        self.udp_port = 12346
        self.majors_avail = [1]
        self.minors_avail = [6,7,8,9,10]
        self.data_interval = 1000
        self.n_diff_anchors_ratio = 0.75
        self.alpha = 0.9722921
        self.TxPower = -66.42379
        self.udp_dao = udpy.UDP_DAO(self.udp_address, self.udp_port)
        self.n_diff_anchors = math.ceil(len(self.minors_avail)*self.n_diff_anchors_ratio)
        self.avg_time = 0

    def count_n_diff_anchors(self,distances):
        minors = []
        for d in distances:
            if d['minor'] not in minors:
                minors.append(d['minor'])
        return len(minors)

    def getData(self):
        return ast.literal_eval(self.udp_dao.readData())

    def getLocation(self):
        distances = []
        ts_milli = time.time() * 1000
        data = self.getData()
        if data['major'] in self.majors_avail and (data['minor'] in self.minors_avail):
            dist = round(10.0 ** (( self.TxPower - data['rssi'] )/(10.0 * self.alpha)), 2)
            data['dist'] = dist
            distances.append(data)
            while (data['timestamp'] - ts_milli) < self.data_interval or self.count_n_diff_anchors(distances) < self.n_diff_anchors:
                data = self.getData()
                if data['major'] in self.majors_avail and (data['minor'] in self.minors_avail):
                    dist = round(10.0 ** (( self.TxPower - data['rssi'] )/(10.0 * self.alpha)), 2)
                    data['dist'] = dist
                    distances.append(data)
                    print  'minor: ' + str(data['minor']) + ' - rssi: ' + str(data['rssi']) + ' - time: ' + str(data['timestamp']) + ' - dist: ' + str(dist)
            print 'distances: ', len(distances)
            location = {'x' : random.uniform(0.0, 5.0), 'y' : random.uniform(0.0, 5.0), 'z' : random.uniform(0.0, 5.0)}
            return location
