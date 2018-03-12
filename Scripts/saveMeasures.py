import pymongo as pm
import UDP_Connection as udp
import beacons as bc
import time

mongo = pm.MongoClient()
db = mongo.beacons
collection = db.measures

beacons = bc.getBeaconsList()

position = {}
position['x'] = 115
position['y'] = 240
position['z'] = 2



count = 0

while True:
    measure_received = udp.getData('127.0.0.1',12346)
    tx_power = -4 # data['measuredPower']
    rssi = measure_received['rssi']
    d = 10.0 ** ((tx_power - rssi) / 20.0)

    measure = {}
    measure['rssi'] = rssi
    measure['estimatedDistance'] = d
    measure['measuredPower'] = measure_received['measuredPower']
    measure['proximity'] = measure_received['proximity']


    uuid = measure_received['uuid']
    major = measure_received['major']
    minor = measure_received['minor']
    b_id = {}
    b_id['uuid'] = uuid
    b_id['major'] = major
    b_id['minor'] = minor
    beacon =  (b for b in beacons if b['id'] == b_id).next()

    measure['beacon'] = beacon
    timestamp = {}
    millis =  time.time()
    timestamp['time'] = millis
    timestamp['readable'] = time.ctime(millis)
    measure['timestamp'] = timestamp

    measure['realPosition'] = position

    collection.insert(measure)

    count +=1

    print "Inserted: ",count
