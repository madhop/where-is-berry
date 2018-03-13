import udpy
import ast

udp_dao = udpy.UDP_DAO('127.0.0.1', 12346)

while True:
    data = udp_dao.read_data()
    print 'qui'
    # convert in dictionary
    data_dic = ast.literal_eval(data)
    if data_dic['major'] == 1 and (data_dic['minor'] == 1 or data_dic['minor'] == 2 or data_dic['minor'] == 3 or data_dic['minor'] == 4):
        print  'rssi: ' + str(data_dic['rssi']) + ' - minor: ' + str(data_dic['minor']) + ' - timestamp: ' + str(data_dic['timestamp'])
