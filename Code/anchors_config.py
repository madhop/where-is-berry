import anchor as a

'''input_list = [{ 'id' : {'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 1}, 'coordinates':{'x':0, 'y': 0, 'z':0}},
{'id' :{'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 2},'coordinates': {'x':1.65, 'y': 0, 'z':0}},
{'id' :{'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 3},'coordinates': {'x':1.65, 'y': 0.7, 'z':0}},
{'id' :{'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 4},'coordinates': {'x':0, 'y': 0.7, 'z':0}},
{'id' :{'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 5},'coordinates': {'x':1.2, 'y': 0.35, 'z':0}}]'''

input_list = [{ 'id' : {'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 1}, 'coordinates':{'x':0, 'y': 0, 'z':0}},
            { 'id' : {'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 2}, 'coordinates':{'x':1.09, 'y': 0, 'z':0}},
            { 'id' : {'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 3}, 'coordinates':{'x':1.09, 'y': 0.74, 'z':0}},
            { 'id' : {'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 4}, 'coordinates':{'x':0, 'y': 0.74, 'z':0}},
            { 'id' : {'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 5}, 'coordinates':{'x':0, 'y': 0.37, 'z':0}}]

anchors = {'anchors_ids': [],
'anchors': {}}
for l in input_list:
    anchor = a.Anchor(l['id'], l['coordinates'])
    _id = anchor.getID()
    anchors['anchors'][_id] = anchor
    anchors['anchors_ids'].append(_id)

anchors['idKeys'] = anchors['anchors'].itervalues().next().id.keys()


def getAnchors():
    return anchors
