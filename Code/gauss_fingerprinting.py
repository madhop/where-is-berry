from pymongo import MongoClient
from scipy import stats
import numpy as np
import anchor as a
import anchors_config as ac
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import plotly.plotly as py
import math

map_name = 'test'

#anchors
anc = ac.getAnchors()
anchors = anc['anchors']
anchors_ids = anc['anchors_ids']
anchor_id_keys = anc['idKeys']

#get mongo collection
mongo = MongoClient()
db = mongo.fingerprinting   # db
map = db[map_name]    # collection

# for each coordinates build gaussian - mu and sigma
coords = map.find().distinct('coords')
gaussians = []  # list of gaussian distributions; 1 for each coordinate
for c in coords:
    l = []
    for a in anchors_ids:
        print a
        tuples = map.find({'coords': {"y" : c['y'], "x" : c['x'], "z" : c['z']}, 'id': a})
        row = [t['rssi'] for t in tuples]
        l.append(row)

    l = np.asarray(l)
    print 'l\n', np.shape(l)

    #GAUSSIAN MEAN AND COVARIANCE
    mu = np.mean(l, axis = 1)
    cov = np.cov(l)
    print 'mean:', mu
    #print 'cov:', cov
    gaussian = {'mu' : mu, 'cov': cov}

    gaussians.append(gaussian)



'''
#PLOT 1D GAUSSIAN
mu1 = mu[0]
mu2 = mu[1]
sigma1 = math.sqrt(cov[0][0])
sigma2 = math.sqrt(cov[1][1])
x1 = np.linspace(mu1 - 3*sigma1, mu1 + 3*sigma1, 100)
x2 = np.linspace(mu2 - 3*sigma2, mu2 + 3*sigma2, 100)
plt.plot(x1,mlab.normpdf(x1, mu1, sigma1))
plt.plot(x2,mlab.normpdf(x2, mu2, sigma2))
plt.show()
'''


'''x = np.array([1,1,1])
mu = np.array([0,0,0])
sigma = np.array([[1,0,0],[0,1,0],[0,0,1]])
m_dist_x = np.dot((x-mu).transpose(),np.linalg.inv(sigma))
m_dist_x = np.dot(m_dist_x, (x-mu))
res = 1-stats.chi2.cdf(m_dist_x, 3)
print 'res', res'''

x = np.array([1,1])
mu1 = np.array([0,0])
mu2 = np.array([2,0])
sigma1 = np.array([[2,1],[1,1]])
sigma2 = np.array([[2,0],[0,1]])
m_dist_x1 = np.dot((x-mu1).transpose(),np.linalg.inv(sigma1))
m_dist_x1 = np.dot(m_dist_x1, (x-mu1))
m_dist_x2 = np.dot((x-mu2).transpose(),np.linalg.inv(sigma2))
m_dist_x2 = np.dot(m_dist_x2, (x-mu2))
res1 = 1-stats.chi2.cdf(m_dist_x1, 1)
res2 = 1-stats.chi2.cdf(m_dist_x2, 1)
print 'res1', res1
print 'res2', res2
