from numpy.linalg import inv

class Kalman:
    def __init__(self):
        #x(k-1|k-1)
        self.last_x
        #P(k-1|k-1)
        self.last_P

    def prediction(self, z, u = 0, F, H, Q, G, R, B = None, n):    #z(k) - measurement vector, u(k) - control input vector, B(k) - control input model
        #PREDICTION STEP
        x_hat = F.dot(self.last_x) + B.dot(u)   #x(k|k-1)
        P_hat = F.dot(last_P).dot(F.T) + Q   #P(k|k-1) - state covariance matrix
        #MEASUREMENT STEP
        y = z - H.dot(x)    #y(k) - error vector
        S = H.dot(P_hat).dot(H.T) + R   #S(k) - innovation matrix
        #UPDATE STATE
        K = P_hat.dot(H.T).dot(inv(S))#K(k) - Kalman gain
        x = x_hat + K.dot(y)    #x(k|k)
        P = (np.eye(n), K.dot(H)).dot(P_hat) #P(k|k)
        self.last_x = x
        self.last_P = P
        return x_hat
