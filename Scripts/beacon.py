class Beacon:
    def __init__(self,uuid,major,minor,x,y,z = 0):
        self.uuid = uuid
        self.major = major
        self.minor = minor
        self.x = x
        self.y = y
        self.z = z
        self.measures = []


class Measure:
    def __init__(self, rssi, distance, timestamp):
        self.rssi = rssi
        self.distance = distance
        self.timestamp = timestamp
