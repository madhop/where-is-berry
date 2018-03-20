import anchor as a

input_list = [{ 'id' : {'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 4, 'minor': 10}, 'coordinates':{'x':3, 'y': 3, 'z':0}},
{'id' :{'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 7},'coordinates': {'x':3, 'y': 67, 'z':0}},
{'id' :{'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 3},'coordinates': {'x':100, 'y': 3, 'z':0}},
{'id' :{'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 2},'coordinates': {'x':100, 'y': 67, 'z':0}},
{'id' :{'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 6},'coordinates': {'x':50, 'y': 50, 'z':0}},
{'id' :{'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 1},'coordinates': {'x':25, 'y': 25, 'z':0}},
{'id' :{'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 8},'coordinates': {'x':25, 'y': 25, 'z':0}}]

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
