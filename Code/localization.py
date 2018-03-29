import numpy as np
import math

class Localization:
    def __init__(self):
        pass

    #Trilateration
    def trilateration(self, data):
        last = data[-1]
        A = np.empty((0,len(last['coordinates'])), dtype=float)
        b = np.empty((0,1), dtype=float)
        for d in data[:-1]:
            A_row = []
            b_row = ((d['dist'] ** 2) - (last['dist'] ** 2) )
            for c in d['coordinates']:
                A_row.append( last['coordinates'][c] - d['coordinates'][c] )
                b_row -= ((d['coordinates'][c] ** 2) - (last['coordinates'][c] **2))
            A = np.append(A, [A_row], axis = 0)
            b = np.append(b, [[b_row]], axis=0)
        print "A", A
        print "b", b
        ls = np.linalg.lstsq(2*A,b)
        pos = {}
        i = 0
        for c in last['coordinates']:
            pos[c] = ls[0][i][0]
            i += 1
        return pos

    def fingerprinting(self):
        pass
