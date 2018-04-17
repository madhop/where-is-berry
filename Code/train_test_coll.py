from pymongo import MongoClient
import time
import anchors_config as ac
import numpy as np

class TrainTestCollections:
    """
    Given a path (sequence of coordinates)
    it creates 2 new collections in mongodb:
        - test: all measurements of the path
        - train: what is not in test
    """
    def __init__(self, path, map_name):
        print 'CREATE TRAIN AND TEST COLLECTIONS'
        self.train_map_name = 'train'
        self.test_map_name = 'test'
        self.path = path
        #get mongo collection
        mongo = MongoClient()
        self.db = mongo.fingerprinting   # db
        map = self.db[map_name]    # collection

        start = time.time()
        # drop old test and train collections
        self.db[self.train_map_name].drop()
        self.db[self.test_map_name].drop()

        # copy the whole map in train
        map.aggregate([{"$out":'train'}])

        # for each position in path insert in test and delete from train
        for p in path:
            tuples = map.find({'coords': {"y" : p['y'], "x" : p['x'], "z" : p['z']}})
            self.db[self.test_map_name].insert(tuples)
            self.db[self.train_map_name].remove({'coords': {"y" : p['y'], "x" : p['x'], "z" : p['z']}})

        end = time.time()
        print 'It took', end - start, 's'

    # create collection that for each position stores the rssi avg from every anchor
    def train_means_coll(self):
        #anchors
        anc = ac.getAnchors()
        anchors = anc['anchors']
        anchors_ids = anc['anchors_ids']
        # drop old
        self.db['train_means'].drop()
        train_map = self.db[self.train_map_name]
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
            rssi_mean = rssi_mean.tolist()
            mean = {'rssi' : rssi_mean, 'coords' : c}
            rssi_means.append(mean)
        #insert in mongo
        self.db['train_means'].insert(rssi_means)
        # END 'train_means_coll' METHOD

    # END CLASS TrainTestCollections


map_name = 'luca_01'
coords = [{'x' : 0.74 ,'y' : 3.69,'z' : 0.41},
            {'x' : 1.065,'y' : 3.29,'z' : 0.41},
            {'x' : 1.39,'y' : 3.29,'z' : 0.41},
            {'x' : 1.715,'y' : 3.29,'z' : 0.41},
            {'x' : 2.04,'y' : 2.89,'z' : 0.41},
            {'x' : 1.715,'y' : 2.49,'z' : 0.41},
            {'x' : 1.39,'y' : 2.49,'z' : 0.41},
            {'x' : 1.065,'y' : 2.09,'z' : 0.41},
            {'x' : 1.39,'y' : 1.69,'z' : 0.41},
            {'x' : 1.715,'y' : 1.69,'z' : 0.41},
            {'x' : 2.04,'y' : 1.69,'z' : 0.41},
            {'x' : 2.365,'y' : 1.29,'z' : 0.41},
            {'x' : 2.365,'y' : 0.89,'z' : 0.41},
            {'x' : 2.69,'y' : 0.89,'z' : 0.41},
            {'x' : 3.015,'y' : 1.29,'z' : 0.41}]
create_colls = TrainTestCollections(coords, map_name)
create_colls.train_means_coll()
