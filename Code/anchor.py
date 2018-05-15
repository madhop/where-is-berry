class Anchor:
    def __init__(self,_id,coordinates, tx_rate):
        self.id = _id
        self.coordinates = coordinates
        self.measures = []
        self.tx_rate = tx_rate

    def getID(self):
        _id = ''
        for i in self.id.keys()[:-1]:
            _id += str(self.id[i]) + ':'
        _id += str(self.id[self.id.keys()[-1]])
        return _id


class Measure:
    def __init__(self, rssi, distance, timestamp):
        self.rssi = rssi
        self.distance = distance
        self.timestamp = timestamp
