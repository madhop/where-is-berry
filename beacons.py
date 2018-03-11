uuid = "b9407f30f5f8466eaff925556b57fe6d"

def spawnBeacon(color, uuid, major, minor, x, y, z):
    beacon = {}
    beacon['color'] = color
    beacon['id'] = {}
    beacon['id']['uuid'] = uuid
    beacon['id']['major'] = major
    beacon['id']['minor'] = minor
    beacon['position'] = {}
    beacon['position']['x'] = x
    beacon['position']['y'] = y
    beacon['position']['z'] = z
    return beacon

def getBeaconsList():
    beacons = []
    beacons.append(spawnBeacon('pink', uuid, 30085, 60205, 160, 398, 110))
    beacons.append(spawnBeacon('purple', uuid, 56653, 61150, 320, 265, 52))
    beacons.append(spawnBeacon('green', uuid, 42622, 48183, 5, 198, 54))
    beacons.append(spawnBeacon('yellow', uuid, 534, 21618, 272, 5, 73))
    beacons.append(spawnBeacon('white', uuid, 49242, 41078, 438, 137, 55))
    return beacons

def getBeaconsDict():
    beacons = {}
    beacons['pink'] = spawnBeacon('pink', uuid, 30085, 60205, 160, 398, 110)
    beacons['purple'] = spawnBeacon('purple', uuid, 56653, 61150, 320, 265, 52)
    beacons['green'] = spawnBeacon('green', uuid, 42622, 48183, 5, 198, 54)
    beacons['yellow'] = spawnBeacon('yellow', uuid, 534, 21618, 272, 5, 73)
    beacons['white'] = spawnBeacon('white', uuid, 49242, 41078, 438, 137, 55)
    return beacons
