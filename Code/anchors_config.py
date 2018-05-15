import anchor as a
import csv
import pprint
import json

config = json.load(open('../Config/config.json'))
filePath = config['filePath']

anchors = {'anchors_ids' : [], 'anchors' : {}}
with open(filePath, 'rb') as f:
    anchorsreader = list(csv.reader(f, delimiter = ','))
    coordinates_index = anchorsreader[0].index('coordinates')
    transmission_rate_index = anchorsreader[0].index('transmission_rate')
    for j in range(2, len(anchorsreader)):
        if len(anchorsreader[j]) > 0:

            _id = {}
            for i in range(0,coordinates_index):
                _id[anchorsreader[1][i]] = anchorsreader[j][i]

            coordinates = {}
            for i in range(coordinates_index, transmission_rate_index):
                coordinates[anchorsreader[1][i]] = float(anchorsreader[j][i])

            tx_rate = anchorsreader[j][transmission_rate_index]

            anchor = a.Anchor(_id, coordinates, tx_rate)
            anchor_id = anchor.getID()
            anchors['anchors'][anchor_id] = anchor
            anchors['anchors_ids'].append(anchor_id)


anchors['idKeys'] = anchors['anchors'].itervalues().next().id.keys()

for a in anchors['anchors']:
    print 'Anchors:'
    print 'id:', anchors['anchors'][a].id, '; coords:', anchors['anchors'][a].coordinates

def getAnchors():
    return anchors
