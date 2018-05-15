#import where_is_berry as wib
from pymongo import MongoClient
import where_is_berry_simulation as wib
import DAO
import matplotlib.pyplot as plt
import pprint
import ast
import math

#get mongo collection
mongo = MongoClient()
db = mongo.fingerprinting   # db
errors_mongo = db['errors_mongo_2']    # collection where we save the estimation errors

'''
TECHNIQUES:
'''
techniques = ['localization_trilateration_kalman',
                'localization_trilateration_unfiltered',
                'localization_fingerprinting_kalman',
                'localization_fingerprinting_unfiltered']

# read actual coordinates, send by simulate_udp_mean
dao_coords = DAO.UDP_DAO("localhost", 12349)

# write on UDP, read by html
dao = DAO.UDP_DAO("localhost", 12347)

berry = wib.WhereIsBerry(12348)

errors = {}
for t in techniques:
    errors[t] = []


while True:
    # read coords
    coords = ast.literal_eval(dao_coords.readData())
    print 'actual_coords', coords
    # location contains the estimated location for all the techniques
    location = berry.whereIsBerry(True)
    if location['message'] == 0:
        break

    # for each techniques conpute estimation error
    for t in techniques:
        estimation = location['localizations'][t]['location']
        error = math.sqrt((estimation['x'] - coords['x']) ** 2 + (estimation['y'] - coords['y']) ** 2 + (estimation['z'] - coords['z']) ** 2)
        print 'error', t, ':', error
        errors[t].append(error)
    print 'errors length', len(errors[techniques[0]])



print 'FINITO'
errors_mongo.insert(errors)


'''
unfiltered_errors = []
kalman_errors = []
# Trilateration unfiltered
while True:
    # read coords
    coords = ast.literal_eval(dao_coords.readData())
    print coords
    location = berry.whereIsBerry(True)
    #pprint.pprint(location)

    # compute euclidean distance between actual position and estimation
    estimation = location['localizations']['localization_unfiltered']['location']
    unfiltered_error = math.sqrt((estimation['x'] - coords['x']) ** 2 + (estimation['y'] - coords['y']) ** 2 + (estimation['z'] - coords['z']) ** 2)
    unfiltered_errors.append(unfiltered_error)
    print 'unfiltered_errors', unfiltered_errors
    estimation = location['localizations']['localization_kalman']['location']
    kalman_error = math.sqrt((estimation['x'] - coords['x']) ** 2 + (estimation['y'] - coords['y']) ** 2 + (estimation['z'] - coords['z']) ** 2)
    kalman_errors.append(kalman_error)
    print 'kalman_errors', kalman_errors
    #dao.writeData(location)'''
