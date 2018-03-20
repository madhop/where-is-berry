from numpy.linalg import inv
import numpy as np

class Kalman:
    def __init__(self, x0, P0):
        #x(k-1|k-1)
        self.last_x_posteriori = x0
        #P(k-1|k-1)
        self.last_P_posteriori = P0
        self.n = (x0.size)/2

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
        #print 'S', S
        #UPDATE STATE
        K = P_priori.dot(H.T).dot(inv(S))#K = P_priori.dot(H.T).dot(inv(S))   #K(k) - Kalman gain
        x_posteriori = x_priori + K.dot(y)  #x(k|k)
        P_posteriori = (np.eye(self.n*2) - K.dot(H)).dot(P_priori) #P(k|k)
        self.last_x_posteriori = x_posteriori
        self.last_P_posteriori = P_posteriori
        return x_posteriori
