from pymongo import MongoClient
import ast
import anchor as a
import anchors_config as ac
import where_is_berry as wib
import time
import datetime
import measure


location = 'uni 2.10'
_id = 'uni_1'

#anchors
anc = ac.getAnchors()
anchors = anc['anchors']
anchor_id_keys = anc['idKeys']

#mongo
mongo = MongoClient()
db = mongo.fingerprinting   # db
"""
'models' collection:
    'id': univocal for place and time
    'location': description of the location
    'anchors': dictionary of anchors:
        key: anchor id
        value: coordinates
    'timestamp'
"""
models = db.models  # collection of models of different rooms
assert models.count({'id':_id}) < 1, "There already exist a model with this id: " + _id

# fill model
ts = time.time()
model_anchors = {'location': location, 'anchors': {}, 'timestamp': ts, 'id': _id}
# delete old models if this room is already in the collection
#deletion = db.models.delete_many({'location':location})

#insert new anchors config
for a in anchors:
    model_anchors['anchors'][anchors[a].getID()] = anchors[a].coordinates

models.insert(model_anchors)
