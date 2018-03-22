from numpy.linalg import inv
import numpy as np

class Kalman:
    def __init__(self, x0, P0, history_length):
        #x(k-1|k-1)
        self.last_x_posteriori = x0
        #P(k-1|k-1)
        self.last_P_posteriori = P0
        self.n = (x0.size)/2
        self.estimates_history = [[] for i in range(0,(self.n))]   #inizialization as list of empty lists (as many lists as the number of anchors)
        self.last_time = []
        self.history_length = history_length

    #z(k) - measurement vector
    #u(k) - control input vector
    #B(k) - control input model
    #Q - process noice covariance matrix
    def estimate(self, z, F, H, Q, G, R, u = 0, B = None):
        if B == None:
            B = np.zeros((self.n*2,1))
        #PREDICTION STEP
        x_priori = F.dot(self.last_x_posteriori) + B.dot(u)   #x(k|k-1)
        P_priori = F.dot(self.last_P_posteriori).dot(F.T) + Q   #P(k|k-1) - state covariance matrix
        #MEASUREMENT STEP
        y = z - H.dot(x_priori)    #y(k) - error vector
        S = H.dot(P_priori).dot(H.T) + R    #S(k) - innovation matrix
        print 'S', S
        #UPDATE STATE
        K = P_priori.dot(H.T).dot(np.linalg.pinv(S))#K = P_priori.dot(H.T).dot(inv(S))   #K(k) - Kalman gain
        x_posteriori = x_priori + K.dot(y)  #x(k|k)
        P_posteriori = (np.eye(self.n*2) - K.dot(H)).dot(P_priori) #P(k|k)
        self.last_x_posteriori = x_posteriori
        self.last_P_posteriori = P_posteriori
        self.updateHistory(H,z,x_posteriori)
        return x_posteriori

    def updateHistory(self, H, z, x_posteriori):
        indices = np.where(H.sum(axis = 1) > 0)[0]  # retrieve indices of row of H with a 1
        #for each of them update the history of etimated distances
        for i in indices:
            self.estimates_history[i].append(x_posteriori[2*i][0])
            #if there are enough value, remove oldest
            if len(self.estimates_history[i]) > self.history_length:
                self.estimates_history[i].pop(0)

    def historyMean(self):
        means = [(sum(i)/len(i) if len(i) != 0 else 0) for i in self.estimates_history]
        return means
