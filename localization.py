import udpy
import ast
import numpy as np
import time

udp_dao = udpy.UDP_DAO('127.0.0.1', 12346)

beacon1 = np.array([0 , 0])

majors_avail = [1]
minors_avail = [1,2,3,4,5]
data_interval = 1000
n_diff_anchors = 4

def count_n_diff_anchors(distances):
    minors = []
    for d in distances:
        if d['minor'] not in minors:
            minors.append(d['minor'])
    return len(minors)


avg_time = 0
while True:
    distances = []
    ts_milli = time.time() * 1000
    data = ast.literal_eval(udp_dao.readData())
    if data['major'] in majors_avail and (data['minor'] in minors_avail):
        distances.append(data)
        while (data['timestamp'] - ts_milli) < data_interval or count_n_diff_anchors(distances) < n_diff_anchors:
            data = ast.literal_eval(udp_dao.readData())
            if data['major'] in majors_avail and (data['minor'] in minors_avail):
                distances.append(data)
                #compute distance from the beacon
                dist = 10.0 ** ((- data['rssi'] - (77) )/20.0)#dist = 10.0 ** (-(data['measuredPower'] - data['rssi'])/20.0)
                print  'minor: ' + str(data['minor']) + ' - rssi: ' + str(data['rssi']) + ' - time: ' + str(data['timestamp']) + ' - dist: ' + str(dist)
        print 'distances: ', len(distances)
        end_time = time.time() * 1000
        
        #avg_time = ((end_time - start_time)/(i+1)) + avg_time*(i/(i+1))
        #print 'time: ', end_time-ts_milli
