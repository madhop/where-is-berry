from pymongo import MongoClient
import numpy as np
import anchor as a
import anchors_config as ac
import matplotlib.pyplot as plt
import math

#anchors
anc = ac.getAnchors()
anchors = anc['anchors']
anchors_ids = anc['anchors_ids']
anchor_id_keys = anc['idKeys']

#get mongo collection
mongo = MongoClient()
db = mongo.fingerprinting   # db
map = db.map_uni    # collection

l = []
for a in anchors_ids:
    print a
    tuples = list(map.find({'id':a}))
    row = [t['rssi'] for t in tuples]
    l.append(row)
l = np.asarray(l)

#GAUSSIAN MEAN AND COVARIANCE
mean = np.mean(l, axis = 1)
cov = np.cov(l)

print 'mean:', mean
print 'cov:', cov
#TODO TRY WITH MULTI BEACONS

#PLOT
x = range(-60,-40)
print 'x', x
g = (1/(math.sqrt(cov * 2 * math.pi))) #* np.exp(x-mean[0])
#plt.plot(x, g)
#plt.show()

x = range(1,50)
print np.exp(x)
