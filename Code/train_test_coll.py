from pymongo import MongoClient
import time

class TrainTestCollections:
    """
    Given a path (sequence of coordinates)
    it creates 2 new collections in mongodb:
        - test: all measurements of the path
        - train: what is not in test
    """
    def __init__(self, path, map_name):
        print 'CREATE TRAIN AND TEST COLLECTIONS'
        self.path = path
        #get mongo collection
        mongo = MongoClient()
        db = mongo.fingerprinting   # db
        map = db[map_name]    # collection

        start = time.time()
        # drop old test and train collections
        db['test'].drop()
        db['train'].drop()

        # copy the whole map in train
        map.aggregate([{"$out":'train'}])

        # for each position in path insert in test and delete from train
        for p in path:
            tuples = map.find({'coords': {"y" : p['y'], "x" : p['x'], "z" : p['z']}})
            db['test'].insert(tuples)
            db['train'].remove({'coords': {"y" : p['y'], "x" : p['x'], "z" : p['z']}})

        end = time.time()
        print 'It took', end - start, 's'

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
