import anchors_config as ac
import numpy as np

class Localization:
    def __init__(self):
        self.anchors = ac.getAnchors()

    #construct key
    def get_id(self, data):
        _id = ''
        for i in self.anchors['idKeys'][:-1]:
            _id += str(data[i]) + ':'
        _id += str(data[self.anchors['idKeys'][-1]])
        return _id

    #Trilateration
    def trilateration(self, data):
        print 'TRILATERATION'
        _id = self.get_id(data[-1])      #get _id of the last measure
        last_anchor = self.anchors[_id]  #get last anchor
        last_dist = data[-1]['dist']
        A = np.empty((0,len(last_anchor.coordinates)), dtype=float)
        b = np.empty((0,1), dtype=float)
        for d in data[:-1]:
            _id = self.get_id(d)
            anchor = self.anchors[_id]  #get anchor
            A_row = []
            b_i = (d['dist'] ** 2)
            for c in anchor.coordinates.keys():
                A_row.append( last_anchor.coordinates[c] - anchor.coordinates[c] )
                b_i -= ((anchor.coordinates[c] ** 2) - (last_anchor.coordinates[c] **2))
            A = np.append(A, [A_row], axis = 0)
            b = np.append(b, [[b_i]], axis=0)

        ls = np.linalg.lstsq(2*A,b, rcond=None)
        pos = {}
        i = 0
        for c in anchor.coordinates.keys():
            pos[c] = ls[0][i][0]
            i += 1
        print pos
        return pos

    def fingerprinting(self):
        pass
