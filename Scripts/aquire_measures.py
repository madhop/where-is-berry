import udpy
import csv
import ast

new_file = False #if False append, if True start from the beginning
beacon = [2] #beacon minor
dist = 5 #m
n_data = 1 #number of measurement

udp_dao = udpy.UDP_DAO('127.0.0.1', 12346)

data_export = []
while len(data_export) < n_data:
    data = ast.literal_eval(udp_dao.readData())
    if data['major'] == 1 and data['minor'] in beacon:
        data['dist'] = dist
        data_export.append(data)
        print len(data_export)

#WRITE HEADER
if new_file == True:
    with open('/home/umberto/Desktop/eggs.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        header = []
        for h in data_export[0]:
            header.append(h)
        print 'header', header
        writer.writerow(header)
        for d in data_export:
            row = []
            for i in d:
                row.append(d[i])
            writer.writerow(row)
else:
    with open('/home/umberto/Desktop/eggs.csv', 'ab') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for d in data_export:
            row = []
            for i in d:
                row.append(d[i])
            writer.writerow(row)
