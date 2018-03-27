from pymongo import MongoClient
import ast
import anchor as a
import anchors_config as ac
import where_is_berry as wib
import time
import DAO

min_data_per_anchor = 5

# check if for each anchor there are enogh data
def ok_counts(counts):
    ok = True
    for c in counts:
        if counts[c] < min_data_per_anchor:
            ok = False
            break
    return ok

#anchors
anc = ac.getAnchors()
anchors = anc['anchors']
print [anchors[a].getID() for a in anchors]
anchors_ids = anc['anchors_ids']
anchor_id_keys = anc['idKeys']

#construct key
def get_id(data):
    _id = ''
    for i in anchor_id_keys[:-1]:
        _id += str(data[i]) + ':'
    _id += str(data[anchor_id_keys[-1]])
    return _id


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
for a in anchors:
    model_anchors['anchors'][anchors[a].getID()] = anchors[a].coordinates

models.insert(model_anchors)


# initialize dictionary of counts
counts = {}
for a in anchors:
    counts[anchors[a].getID()] = 0

#get data form udp
dao = DAO.UDP_DAO("localhost", 12346)

pi_pos = {'x':0.5,'y':0.5,'z':0}
while not ok_counts(counts):    #TODO
    data = ast.literal_eval(dao.readData())
    _id = get_id(data)
    while not anchors.has_key(_id):    #go on only if the first is a good anchor
        data = ast.literal_eval(dao.readData())
        _id = get_id(data)
    doc = {'id': _id, 'timestamp': data['timestamp'], 'rssi': data['rssi'], 'coords': pi_pos}
    map.insert(doc)
    counts[_id] += 1
    print _id, '; count:', counts[_id]

print 'mongoooo'
