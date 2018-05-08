from pymongo import MongoClient
from scipy import stats
import numpy as np
import anchors_config as ac
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import plotly.plotly as py
import math
import pprint

class Fingerprinting:
    """docstring"""
    def __init__(self):
        train_map_name = 'train_means'
        test_map_name = 'test'
        self.k = 9
        #anchors
        anc = ac.getAnchors()
        anchors = anc['anchors']
        anchors_ids = anc['anchors_ids']
        #get mongo collection
        mongo = MongoClient()
        db = mongo.fingerprinting   # db
        train_map = db[train_map_name]    # train collection
        #test_map = db[test_map_name]    # test collection

        self.rssi_means = list(train_map.find())  # list of lists rssi averages; 1 list for each coordinate
        print 'Fingerprinting'
        # END __init__

    def knn(self, data):
        print '**************knn'

        wiwtbp = [d['rssi'] for d in data]
        wiwtbp = np.asarray(wiwtbp)

        #compute euclidean distance from every position in train set
        eu_distances = []
        for rm in self.rssi_means:
            euclidean_dist = np.linalg.norm( wiwtbp - rm['rssi'] )
            #print 'euclidean_dist', euclidean_dist, " ", rm['coords']
            d = {'eu_dist' : euclidean_dist, 'coords' : rm['coords']} #bind train coord with the distance from the point to be tracked
            eu_distances.append(d)

        # sort
        eu_distances = sorted(eu_distances, key = lambda d : d['eu_dist'], reverse = False)
        #print 'sorted by euclidean distance'
        #pprint.pprint(eu_distances)

        # take k closer coordinates
        knearest = eu_distances[:self.k]
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
        return position_hat
