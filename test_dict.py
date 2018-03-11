import numpy as np
import beacons as bn

point = {}
point['x'] = 260
point['y'] = 200
point['z'] = 55

beacons = bn.getBeaconsDict()

distance = {}

for color in beacons:
    b = beacons[color]
    distance[color] = np.sqrt((point['x']-b['position']['x'])**2 + (point['y']-b['position']['y'])**2 + (point['z']-b['position']['z'])**2)

A = 2*np.array([[beacons['pink']['position']['x'] - beacons['yellow']['position']['x'],
                beacons['pink']['position']['y'] - beacons['yellow']['position']['y'],
                beacons['pink']['position']['z'] - beacons['yellow']['position']['z']
                ],[
                beacons['pink']['position']['x'] - beacons['green']['position']['x'],
                beacons['pink']['position']['y'] - beacons['green']['position']['y'],
                beacons['pink']['position']['z'] - beacons['green']['position']['z']
                ],[
                beacons['pink']['position']['x'] - beacons['purple']['position']['x'],
                beacons['pink']['position']['y'] - beacons['purple']['position']['y'],
                beacons['pink']['position']['z'] - beacons['purple']['position']['z']
                ],[
                beacons['pink']['position']['x'] - beacons['white']['position']['x'],
                beacons['pink']['position']['y'] - beacons['white']['position']['y'],
                beacons['pink']['position']['z'] - beacons['white']['position']['z']
                ]])
y = np.array([[(distance['yellow']**2 - distance['pink']**2) -
                (beacons['yellow']['position']['x']**2 - beacons['pink']['position']['x']**2) -
                (beacons['yellow']['position']['y']**2 - beacons['pink']['position']['y']**2) -
                (beacons['yellow']['position']['z']**2 - beacons['pink']['position']['z']**2)],
                [(distance['green']**2 - distance['pink']**2) -
                (beacons['green']['position']['x']**2 - beacons['pink']['position']['x']**2) -
                (beacons['green']['position']['y']**2 - beacons['pink']['position']['y']**2) -
                (beacons['green']['position']['z']**2 - beacons['pink']['position']['z']**2)],
                [(distance['purple']**2 - distance['pink']**2) -
                (beacons['purple']['position']['x']**2 - beacons['pink']['position']['x']**2) -
                (beacons['purple']['position']['y']**2 - beacons['pink']['position']['y']**2) -
                (beacons['purple']['position']['z']**2 - beacons['pink']['position']['z']**2)],
                [(distance['white']**2 - distance['pink']**2) -
                (beacons['white']['position']['x']**2 - beacons['pink']['position']['x']**2) -
                (beacons['white']['position']['y']**2 - beacons['pink']['position']['y']**2) -
                (beacons['white']['position']['z']**2 - beacons['pink']['position']['z']**2)]
                ])

x = np.linalg.pinv(A).dot(y)


print x
