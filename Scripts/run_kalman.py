import udpy
import localization

localization = localization.Localization()

udp = udpy.UDP_DAO("localhost",12347)

while True:
    data = udp.readData()
    print data
    n = 6

    delta_t = 0
    #F(k) - state transition model
    F = np.zeros((2*n,2*n))
    for i in range(1,2*n,2):
        F[i-1][i-1] = 1
        F[i-1][i] = delta_t
        F[i][i] = 1

    #H(k) - observation model
    H = np.zeros((n,2*n))
    #TODO
    '''for i in range(0,2*n,2):
        H[i][i] = 1'''

    #Q(k) - process noise covarinace matrix
    Q = np.zeros((2*n,2*n))
    for i in range(1,2*n,2):
        Q[i-1][i-1] = 1
        Q[i-1][i] = 1
        Q[i][i] = 1

    G = 100 #gain
    delta_d = np.zeros((n)) #d - history_mean_d
    #R(k) - measurement noise matrix
    R = np.zeros((n,n))
    for i in range(0,n):
        R[i][i] = delta_d[i] * G
