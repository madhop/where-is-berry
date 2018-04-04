from pymongo import MongoClient
import ast
import anchor as a
import anchors_config as ac
import where_is_berry as wib
import time
import DAO
import measure


map_name = 'test2'  # must match with the id of a model
pi_pos = {'x':0.2,'y':0,'z':0}    #position of the device in the map
data_per_anchor = 150

#anchors
anc = ac.getAnchors()
anchors = anc['anchors']
anchor_id_keys = anc['idKeys']

#mongo
mongo = MongoClient()
db = mongo.fingerprinting   # db

# collection of models of different rooms
models = db.models
#assert models.count({ 'id' : map_name }) == 1, "No model with this id: " + map_name
# collection where to insert the 'rssi's
map = db[map_name]

# initialize dictionary of counts
counts = {}
for a in anchors:
    counts[anchors[a].getID()] = 0

#get data form udp
dao = DAO.UDP_DAO("localhost", 12346)

#for each anchor store 'data_per_anchor' rssi
tuples = []
while False in [counts[c] >= data_per_anchor for c in counts]:
    data = ast.literal_eval(dao.readData())
    _id = measure.get_id(data,anchor_id_keys)
    while not anchors.has_key(_id):    #go on only if the first is a good anchor
        data = ast.literal_eval(dao.readData())
        _id = measure.get_id(data, anchor_id_keys)
    if counts[_id] < data_per_anchor:
        doc = {'id': _id, 'timestamp': data['timestamp'], 'rssi': data['rssi'], 'coords': pi_pos}
        tuples.append(doc)
        counts[_id] += 1
    print _id, '; count:', counts[_id]

map.insert(tuples)


print 'mongo'
