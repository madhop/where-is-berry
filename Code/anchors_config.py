import anchor as a


input_list = [{ 'id' : {'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 10}, 'coordinates':{'x':0.40, 'y': 0, 'z':0}}]

'''input_list = [{ 'id' : {'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 10}, 'coordinates':{'x':1, 'y': 0.1, 'z':0}},
                 { 'id' : {'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 7},'coordinates': {'x': 1, 'y': 0.8, 'z':0}},
                 { 'id' : {'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 8},'coordinates': {'x': 0.2, 'y': 0.1, 'z':0}},
                 { 'id' : {'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 9},'coordinates': {'x': 1, 'y': 0.8, 'z':0}},
                 { 'id' : {'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 6},'coordinates': {'x': 0, 'y': 1, 'z':0}}]
'''


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
