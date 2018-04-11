from pymongo import MongoClient
import numpy as np
import anchor as a
import anchors_config as ac
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import plotly.plotly as py
import math

map_name = 'test2'

#anchors
anc = ac.getAnchors()
anchors = anc['anchors']
anchors_ids = anc['anchors_ids']
anchor_id_keys = anc['idKeys']

#get mongo collection
mongo = MongoClient()
db = mongo.fingerprinting   # db
map = db[map_name]    # collection

l = []
for a in anchors_ids:
    print a
    tuples = map.find({'id':a})
    print 'size', map.count({'id':a})
    row = [t['rssi'] for t in tuples]
    
    l.append(row)
l = np.asarray(l)
print 'l\n', l

#GAUSSIAN MEAN AND COVARIANCE
mu = np.mean(l, axis = 1)
cov = np.cov(l)

print 'mean:', mu
print 'cov:', cov

#PLOT GAUSSIAN
mu1 = mu[0]
mu2 = mu[1]
sigma1 = math.sqrt(cov[0][0])
sigma2 = math.sqrt(cov[1][1])
x1 = np.linspace(mu1 - 3*sigma1, mu1 + 3*sigma1, 100)
x2 = np.linspace(mu2 - 3*sigma2, mu2 + 3*sigma2, 100)
plt.plot(x1,mlab.normpdf(x1, mu1, sigma1))
plt.plot(x2,mlab.normpdf(x2, mu2, sigma2))
plt.show()
