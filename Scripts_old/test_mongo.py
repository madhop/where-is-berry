import numpy as np
import beacons as bn
import pymongo as pm
import pprint
import data

mongo = pm.MongoClient()
db = mongo.beacons
collection = db.measures

'''
position['x'] = 250
position['y'] = 35
position['z'] = 73

position['x'] = 115
position['y'] = 240
position['z'] = 2

position['x'] = 280
position['y'] = 210
position['z'] = 53
'''

condition = {'realPosition' : {'x' : 250, 'y' : 35, 'z' : 73}}

measures = data.getDataMongo("localhost", "default", "beacons", "measures", condition, 10)

A = np.empty([0,3])
y = np.empty([0,1])
for i in range(0, len(measures)-1):
    if measures[len(measures)-1]['beacon'] != measures[i]['beacon']:
        A_row = 2*np.array([measures[len(measures)-1]['beacon']['position']['x'] - measures[i]['beacon']['position']['x'],
                        measures[len(measures)-1]['beacon']['position']['y'] - measures[i]['beacon']['position']['y'],
                        measures[len(measures)-1]['beacon']['position']['z'] - measures[i]['beacon']['position']['z']])
        A = np.vstack((A,A_row))
        y_row = np.array([((measures[i]['estimatedDistance']/10)**2 - (measures[len(measures)-1]['estimatedDistance']/10)**2) -
                        (measures[i]['beacon']['position']['x']**2 - measures[len(measures)-1]['beacon']['position']['x']**2) -
                        (measures[i]['beacon']['position']['y']**2 - measures[len(measures)-1]['beacon']['position']['y']**2) -
                        (measures[i]['beacon']['position']['z']**2 - measures[len(measures)-1]['beacon']['position']['z']**2)
                        ])
        y = np.vstack((y,y_row))

x = np.linalg.pinv(A).dot(y)
print x
