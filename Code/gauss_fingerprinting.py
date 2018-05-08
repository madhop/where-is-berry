from pymongo import MongoClient
from scipy import stats
import numpy as np
import anchor as a
import anchors_config as ac
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import plotly.plotly as py
import math
import pprint

train_map_name = 'train' #'luca_01'
test_map_name = 'test'

#anchors
anc = ac.getAnchors()
anchors = anc['anchors']
anchors_ids = anc['anchors_ids']
anchor_id_keys = anc['idKeys']

#get mongo collection
mongo = MongoClient()
db = mongo.fingerprinting   # db
train_map = db[train_map_name]    # train collection
test_map = db[test_map_name]    # test collection

# for each coordinates build gaussian - mu and sigma
coords = train_map.find().distinct('coords')
gaussians = []  # list of gaussian distributions; 1 for each coordinate
for c in coords:
    print 'train_cooord:', c
    l = []
    for a in anchors_ids:
        tuples = train_map.find({'coords': {"y" : c['y'], "x" : c['x'], "z" : c['z']}, 'id': a})
        row = [t['rssi'] for t in tuples]
        l.append(row)

    l = np.asarray(l)

    #GAUSSIAN MEAN AND COVARIANCE
    mu = np.mean(l, axis = 1)
    cov = np.cov(l)
    #print 'mean:', mu
    #print 'cov:', cov
    gaussian = {'mu' : mu, 'cov': cov, 'coords' : c}
    #print 'gaussian', gaussian

    gaussians.append(gaussian)
    print 'gaussians', len(gaussians)


# given a positon, tell at which gaussian it belongs to
l = []
for a in anchors_ids:
    tuples = test_map.find({'coords': {"y" : 3.69, "x" : 0.74, "z" : 0.41}, 'id': a})
    row = [t['rssi'] for t in tuples]
    l.append(row)
l = np.asarray(l)

# position I wnat to find
x = np.mean(l, axis = 1)
print 'x', x

# given the position 'x', tell the probability to belong to each gaussian
probabilities = []  # list of dictionanries of coordinate and probability
for g in gaussians:
    # Mahalanobis distance
    m_dist_x = np.dot((x-g['mu']).transpose(),np.linalg.inv(g['cov']))
    m_dist_x = np.dot(m_dist_x, (x-g['mu']))

    # probability to belong to this gaussian
    prob = 1-stats.chi2.cdf(m_dist_x, 8)
    p = {'prob' : prob, 'coords' : g['coords']}
    probabilities.append(p)

print 'probabilities\n', probabilities
# sort by probability
probabilities = sorted(probabilities, key = lambda p : p['prob'], reverse = True)
print 'sorted probabilities\n'
pprint.pprint(probabilities)




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
