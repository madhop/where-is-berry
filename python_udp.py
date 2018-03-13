import socket
import ast

UDP_IP = "127.0.0.1"
UDP_PORT = 1234

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    # convert in dictionary
    data_dic = ast.literal_eval(data)
    if data_dic['major'] == 1 and (data_dic['minor'] == 1 or data_dic['minor'] == 2 or data_dic['minor'] == 3 or data_dic['minor'] == 4):
        print  'rssi: ' + str(data_dic['rssi']) + ' - minor: ' + str(data_dic['minor'])
