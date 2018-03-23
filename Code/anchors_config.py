import anchor as a
import csv
import pprint
import json

config = json.load(open('../Config/config.json'))
filePath = config['filePath']

anchors = {'anchors_ids': [],
'anchors': {}}
with open(filePath, 'rb') as f:
    anchorsreader = list(csv.reader(f, delimiter = ','))
    index = anchorsreader[0].index('coordinates')
    for j in range(2, len(anchorsreader)):
        if len(anchorsreader[j]) > 0:
            _id = {}
            for i in range(0,index):
                _id[anchorsreader[1][i]] = anchorsreader[j][i]
            coordinates = {}
            for i in range(index, len(anchorsreader[0])):
                coordinates[anchorsreader[1][i]] = float(anchorsreader[j][i])
            anchor = a.Anchor(_id, coordinates)
            anchor_id = anchor.getID()
            anchors['anchors'][anchor_id] = anchor
            anchors['anchors_ids'].append(anchor_id)


anchors['idKeys'] = anchors['anchors'].itervalues().next().id.keys()

def getAnchors():
    return anchors
