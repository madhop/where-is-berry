import numpy as np
import UDP_Connection as udp
import pymongo


while True:
    data = udp.getData('127.0.0.1',12346)
    tx_power = -4 # data['measuredPower']
    rssi = data['rssi']
    d = 10.0 ** ((tx_power - rssi) / 20.0)
    print data, d
