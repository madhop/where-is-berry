from numpy.linalg import inv

class Kalman:
    def __init__(self, x0, P0, history_length):
        #x(k-1|k-1)
        self.last_x_posteriori = x0
        #P(k-1|k-1)
        self.last_P_posteriori = P0
        self.state_dim = x0.size
        self.estimates_history = []
        self.last_time = []

    #z(k) - measurement vector
    #u(k) - control input vector
    #B(k) - control input model
    #Q - process noice covariance matrix
    def estimate(self, z, F, H, Q, G, R, u = 0, B = np.zeros((self.state_dim,1))):
        #PREDICTION STEP
        x_priori = F.dot(self.last_x_posteriori) + B.dot(u)   #x(k|k-1)
        P_priori = F.dot(last_P_posteriori).dot(F.T) + Q   #P(k|k-1) - state covariance matrix
        #MEASUREMENT STEP
        y = z - H.dot(x_priori)    #y(k) - error vector
        S = H.dot(P_priori).dot(H.T) + R    #S(k) - innovation matrix
        #UPDATE STATE
        K = P_priori.dot(H.T).dot(inv(S))   #K(k) - Kalman gain
        x_posteriori = x_priori + K.dot(y)  #x(k|k)
        P_posteriori = (np.eye(n), K.dot(H)).dot(P_priori) #P(k|k)
        self.last_x_posteriori = x_posteriori
        self.last_P_posteriori = P_posteriori
        return x_posteriori

    def updateHistory(self, H, z, x_posteriori):
        
