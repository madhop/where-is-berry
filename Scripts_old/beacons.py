import beacons_config as config

place = 1

def spawnBeacon(color, b_id, position):
    beacon = {}
    beacon['color'] = color
    beacon['id'] = b_id
    beacon['position'] = position
    return beacon


def getBeacons(struct):
    beaconsList = []
    beacons = ""
    colors = config.getColors()
    position = config.getPos(place)
    b_id = config.getId()
    for c in colors:
        beaconsList.append(spawnBeacon(colors[c], b_id[colors[c]], position[colors[c]]))
    if struct == "list":
        beacons = beaconsList
    elif struct == "dict":
        beacons = {}
        for c in colors:
            beacons[colors[c]] = beaconsList[c - 1]
    return beacons
