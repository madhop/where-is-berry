import pymongo
import udpy
import json

db_name = "beacons"
col_name = "measures"

mongo = pymongo.MongoClient()
db = mongo[db_name]
collection = db[col_name]
positions = collection.find().distinct("realPosition")

data = list(collection.find({"realPosition" : positions[0]}))
for d in data:
    del d['_id']

print "Sending to udp..."

udp = udpy.UDP_DAO("localhost",12346)

while True:
    for d in data:
        d = str(json.dumps(d)) #removes the 'u' and convert it to string
        udp.writeData(d)
