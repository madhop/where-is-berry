import data as dm
import json
import ast
import mongo



positions = dm.getDataMongoDistinct("localhost","default","beacons","measures", {}, 100, "realPosition")

data = dm.getDataMongo("localhost","default","beacons","measures", {"realPosition" : positions[0]}, 100)
for d in data:
    del d['_id']

print "Sending to udp..."


while True:
    for d in data:
        d = str(json.dumps(d)) #removes the 'u' and convert it to string
        dm.sendToUDP("localhost",12346,d)
