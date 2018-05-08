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
    def estimate(self, z, F, H, Q, R, u = 0, B = None):
        if B == None:
            B = np.zeros((self.n*2,1))
        #PREDICTION STEP
        x_priori = F.dot(self.last_x_posteriori) + B.dot(u)   #x(k|k-1)
        P_priori = F.dot(self.last_P_posteriori).dot(F.T) + Q   #P(k|k-1) - state covariance matrix
        #print 'P_priori\n',P_priori
        #MEASUREMENT STEP
        y = z - H.dot(x_priori)    #y(k) - error vector
        S = H.dot(P_priori).dot(H.T) + R    #S(k) - innovation matrix
        #print 'S\n', S
        #UPDATE STATE
        K = P_priori.dot(H.T).dot(inv(S))#K = P_priori.dot(H.T).dot(inv(S))   #K(k) - Kalman gain
        #print 'K\n', K
        x_posteriori = x_priori + K.dot(y)  #x(k|k)
        P_posteriori = (np.eye(self.n*2) - K.dot(H)).dot(P_priori) #P(k|k)
        #print 'P_posteriori\n', P_posteriori
        self.last_x_posteriori = x_posteriori
        self.last_P_posteriori = P_posteriori
        return x_posteriori

def filter(data, phi, var):
    n = self.n
    batch_size = len(data)

    ######F(k) - state transition model (static)
    now = data[-1]['timestamp']# np.mean([m['timestamp'] for m in measures])
    if(self.last_time == None):
        self.last_time = now

    delta_t = 0 # (now - self.last_time)/1000.0
    delta_t_list = [delta_t]*(2*n)
    #print 'now', now
    #print 'self.last_time', self.last_time
    #print 'delta_t', delta_t
    F = np.zeros((2*n,2*n))
    for i in range(1,2*n,2):
        F[i-1][i-1] = 1
        F[i-1][i] = delta_t_list[i]
        F[i][i] = 1
    #print 'F', F

    ######Q(k) - process noise covarinace matrix (static)
    phi = 1
    Q = np.zeros((2*n,2*n))
    for i in range(1,2*n,2):
        Q[i-1][i-1] = (delta_t ** 3)/3
        Q[i-1][i] = (delta_t ** 2)/2
        Q[i][i-1] = (delta_t ** 2)/2
        Q[i][i] = delta_t
    Q = Q * phi
    #print 'Q', Q

    ######z(k) - measurement vector (dynamic)
    z = np.empty((batch_size,1))
    ######R(k) - measurement noise matrix (dynamic)
    meas_noise_var = []
    ######H(k) - observation model (dynamic)
    H = np.zeros((batch_size,2*n))
    row_n = 0
    for m in data:
        index = self.anchors_ids.index(m['id'])
        ##z
        z[row_n][0] = m['rssi']
        ##R
        var = 0.5
        meas_noise_var.append(var)
        #H
        H[row_n][(2*index)] = 1
        row_n += 1

    #print 'var', meas_noise_var
    R = np.diag((meas_noise_var))
    #print 'R', R
    #print 'H', H
    #print 'z', z

    #compute kalman filtering
    x = self.kalman_dist.estimate(z, F, H, Q, R)
    return x
