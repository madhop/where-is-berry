#import where_is_berry as wib
import where_is_berry as wib
import DAO
import matplotlib.pyplot as plt
import pprint
import ast
import math

# read actual coordinates, send by simulate_udp_mean
dao_coords = DAO.UDP_DAO("localhost", 12349)

# write on UDP, read by html
dao = DAO.UDP_DAO("localhost", 12347)

berry = wib.WhereIsBerry(12348)

unfiltered_errors = []
kalman_errors = []
last_coords = ast.literal_eval(dao_coords.readData())
# Kalman
while True:
    # read coords
    coords = ast.literal_eval(dao_coords.readData())
    print 'coords', coords
    location = berry.whereIsBerry(True)

    # if it is at the end of a position, compute the error
    if coords != last_coords:
        kalman_error = math.sqrt((estimation['x'] - coords['x']) ** 2 + (estimation['y'] - coords['y']) ** 2 + (estimation['z'] - coords['z']) ** 2)
        kalman_errors.append(kalman_error)
        print 'kalman_errors', kalman_errors
        print 'kalman_errors', len(kalman_errors)
        last_coords = coords

    estimation = location['localizations']['localization_kalman']['location']
'''
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
