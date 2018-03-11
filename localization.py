import numpy as np
import udpConnection as udp


while True:
    data = udp.getData()
    tx_power = -4 # data['measuredPower']
    rssi = data['rssi']
    d = 10.0 ** ((tx_power - rssi) / 20.0)
    print data, d
