from pymongo import MongoClient
import ast
import anchor as a
import anchors_config as ac
import where_is_berry as wib
import time
import DAO
import measure

min_data_per_anchor = 5

#anchors
anc = ac.getAnchors()
anchors = anc['anchors']
anchor_id_keys = anc['idKeys']
print 'ANCHORS:'
print [anchors[a].getID() for a in anchors]

#get mongo collection
mongo = MongoClient()
db = mongo.fingerprinting   # db
"""
'models' collection:
'location': name of the location
'anchors': dictionary of anchors:
    key: anchor id
    value: coordinates
"""
models = db.models  # collection of models of different rooms
map = db.map_uni    # collection

# fill model
ts = time.time()
model_anchors = {'location': 'uni', 'anchors': {}, 'timestamp': ts}
# delete old models if this room is already in the collection
daletion = db.models.delete_many({'location':'uni'})

#insert new anchors config
for a in anchors:
    model_anchors['anchors'][anchors[a].getID()] = anchors[a].coordinates

models.insert(model_anchors)

# initialize dictionary of counts
counts = {}
for a in anchors:
    counts[anchors[a].getID()] = 0

#get data form udp
dao = DAO.UDP_DAO("localhost", 12346)

pi_pos = {'x':0.5,'y':0.5,'z':0}    #position of the device in the map
#from each anchor store 'min_data_per_anchor' rssi
while False in [counts[c] >= min_data_per_anchor for c in counts]:
    data = ast.literal_eval(dao.readData())
    _id = measure.get_id(data,anchor_id_keys)
    while not anchors.has_key(_id):    #go on only if the first is a good anchor
        data = ast.literal_eval(dao.readData())
        _id = measure.get_id(data, anchor_id_keys)
    doc = {'id': _id, 'timestamp': data['timestamp'], 'rssi': data['rssi'], 'coords': pi_pos}
    map.insert(doc)
    counts[_id] += 1
    print _id, '; count:', counts[_id]

print 'mongoooo'
