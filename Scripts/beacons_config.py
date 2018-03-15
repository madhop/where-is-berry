"""
create a list of dictionary:
- key= uuid:major:minor
- value= corresponding beacon 
"""

import beacon as b
import pprint as pp
input_list = [{'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 1, 'x':3, 'y': 3, 'z':0},
{'uuid': "b9407f30f5f8466eaff925556b57fe6d", 'major': 1, 'minor': 4, 'x':3, 'y': 67, 'z':0}]

beacons = {}
for i in input_list:
    _id = i['uuid'] + ':' + str(i['major']) + ':' + str(i['minor'])
    estimote = b.Beacon(i['uuid'], i['major'], i['minor'], x = i['x'], y = i['y'], z = i['z'])
    beacons[_id] = estimote

def estimotes():
    return beacons, [m.minor for m in beacons.values()]
