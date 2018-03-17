import numpy as np
import data as dm
import pymongo as pm
import ast
import json

'''
while True:
    data = data.getDataUDP('127.0.0.1',12346, 1)
    tx_power = -4 # data['measuredPower']
    rssi = data['rssi']
    d = 10.0 ** ((tx_power - rssi) / 20.0)
    print data, d
'''

def estimatePosition(distances):
    A = np.empty([0,3])
    y = np.empty([0,1])
    for i in range(0, len(distances)-1):
        if distances[len(distances)-1]['beacon'] != distances[i]['beacon']:
            A_row = 2*np.array([distances[len(distances)-1]['beacon']['position']['x'] - distances[i]['beacon']['position']['x'],
                            distances[len(distances)-1]['beacon']['position']['y'] - distances[i]['beacon']['position']['y'],
                            distances[len(distances)-1]['beacon']['position']['z'] - distances[i]['beacon']['position']['z']])
            A = np.vstack((A,A_row))
            y_row = np.array([((distances[i]['estimatedDistance']/10)**2 - (distances[len(distances)-1]['estimatedDistance']/10)**2) -
                            (distances[i]['beacon']['position']['x']**2 - distances[len(distances)-1]['beacon']['position']['x']**2) -
                            (distances[i]['beacon']['position']['y']**2 - distances[len(distances)-1]['beacon']['position']['y']**2) -
                            (distances[i]['beacon']['position']['z']**2 - distances[len(distances)-1]['beacon']['position']['z']**2)
                            ])
            y = np.vstack((y,y_row))

    x = np.linalg.pinv(A).dot(y)

    return x


#condition = {'realPosition' : {'x' : 250, 'y' : 35, 'z' : 73}}
#measures = data.getDataMongo("localhost", "default", "beacons", "measures", condition, 10)
samples = 0.0
avgPosition = np.empty([3,1])
while True:
    measures = []
    for i in range(0,5):
        data = dm.getDataUDP("localhost",12346) #get string
        data = ast.literal_eval(data) #Convert string to dictionary
        print data
        measures.append(data)

    #position = estimatePosition(measures)
    #avgPosition = (samples/(samples+1))*avgPosition + position/(samples+1)

    #samples += 1
    #print avgPosition

#(mean * oldsamples + new)/newsamples = mean*(oldsamples/newsamples) + new/newsamples
