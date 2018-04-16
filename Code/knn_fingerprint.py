"""
For each train coordinates, compute averages of rssi from each anchor.
Given a localization (a new measurement from each anchor) find the knn and
find the position as the weighted average of the kn coordinates
"""
from pymongo import MongoClient
from scipy import stats
import numpy as np
import anchors_config as ac
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import plotly.plotly as py
import math
import pprint

train_map_name = 'train'#'test'
test_map_name = 'test'
k = 9

#anchors
anc = ac.getAnchors()
anchors = anc['anchors']
anchors_ids = anc['anchors_ids']

#get mongo collection
mongo = MongoClient()
db = mongo.fingerprinting   # db
train_map = db[train_map_name]    # train collection
test_map = db[test_map_name]    # test collection

# for each train coordinates compute avg rssi from each anchor
coords = train_map.find().distinct('coords')
rssi_means = []  # list of averages; 1 for each coordinate
i = 0
for c in coords:
    print i, 'train coord:', c
    i += 1
    l = []
    for a in anchors_ids:
        tuples = train_map.find({'coords': {"y" : c['y'], "x" : c['x'], "z" : c['z']}, 'id': a})
        row = [t['rssi'] for t in tuples]
        l.append(row)

    l = np.asarray(l)
    rssi_mean = np.mean(l, axis = 1)
    mean = {'rssi' : rssi_mean, 'coords' : c}
    rssi_means.append(mean)
'''
KNN
'''
#neigh = KNeighborsClassifier(n_neighbors = 9)
#neigh.fit(rssi_means,labels)

# for each test position, find knn and compute weighted average
test_coords = test_map.find().distinct('coords')
estimation_error = []
for tc in test_coords:
    print 'test coord', tc
    l = []
    for a in anchors_ids:
        tuples = test_map.find({'coords': {"y" : tc['y'], "x" : tc['x'], "z" : tc['z']}, 'id': a})
        row = [t['rssi'] for t in tuples]
        l.append(row)
    l = np.asarray(l)

    # what I want to be predicted
    wiwtbp = np.mean(l, axis = 1)
    #print 'wiwtbp', wiwtbp

    #compute euclidean distance from every position in train set
    eu_distances = []
    for rm in rssi_means:
        euclidean_dist = np.linalg.norm( wiwtbp - rm['rssi'] )
        #print 'euclidean_dist', euclidean_dist, " ", rm['coords']
        d = {'eu_dist' : euclidean_dist, 'coords' : rm['coords']} #bind train coord with the distance from the point to be tracked
        eu_distances.append(d)

    # sort
    eu_distances = sorted(eu_distances, key = lambda d : d['eu_dist'], reverse = False)
    #print 'sorted by euclidean distance'
    #pprint.pprint(eu_distances)

    # take k closer coordinates
    knearest = eu_distances[:k]
    # if a distance is 0, that is the position
    if knearest[0]['eu_dist'] == 0:
        position_hat = knearest[0]['coords']
        #knearest[0]['eu_dist'] = 0.000000001
    # otherwise compute weighted avg
    else:
        weights_sum = sum( [ 1/kn['eu_dist'] for kn in knearest ] )
        position_hat = {'x' : 0, 'y' : 0, 'z' : 0}
        for kn in knearest:
            weight = (1/kn['eu_dist'])/weights_sum
            for key in kn['coords']:
                position_hat[key] = position_hat[key] + weight * kn['coords'][key]

    print 'position_hat', position_hat
    # compute distance between estimation and correct position
    error = math.sqrt((position_hat['x'] - tc['x']) ** 2 + (position_hat['y'] - tc['y']) ** 2 + (position_hat['z'] - tc['z']) ** 2)
    estimation_error.append(error)

print 'estimation_error', estimation_error
