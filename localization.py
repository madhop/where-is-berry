#Localization

#dev
import udpy
import ast
import numpy

udp_dao = udpy.UDP_DAO('127.0.0.1', 12346)

while True:
    data = udp_dao.readData()
    # convert in dictionary
    data_dic = ast.literal_eval(data)
    if data_dic['major'] == 1 and (data_dic['minor'] == 1 or data_dic['minor'] == 2 or data_dic['minor'] == 3 or data_dic['minor'] == 4 or data_dic['minor'] == 5):
        #conpute distance from the beacon
        dist = 10.0 ** ((data_dic['measuredPower'] - data_dic['rssi'])/20.0)
        x,y
        x_hat, y_hat = kalman(x, y, state)
        print  'minor: ' + str(data_dic['minor']) + ' - rssi: ' + str(data_dic['rssi']) + ' - dist: ' + str(dist)
