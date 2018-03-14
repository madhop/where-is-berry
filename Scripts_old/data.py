import pymongo as pm
import socket
import json

def getDataUDP(address, port):

    UDP_IP = address
    UDP_PORT = port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #return json.loads(data)
    return data

def getDataMongo(address, port, db, collection, condition, batch):
    mongo = pm.MongoClient()
    db = mongo.beacons
    collection = db.measures
    data = list(collection.find(condition).limit(batch))
    return data

def getDataMongoDistinct(address, port, db, collection, condition, batch, dist):
    mongo = pm.MongoClient()
    db = mongo.beacons
    collection = db.measures
    data = list(collection.find(condition).limit(batch).distinct(dist))
    return data

def sendToUDP(address, port, message):
   UDP_IP = address
   UDP_PORT = port
   MESSAGE = message
   sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
