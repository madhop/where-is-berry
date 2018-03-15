import udpy
import csv
import ast

new_file = False #if False append, if True start from the beginning
beacon = 5 #beacon minor
dist = 2 #m
n_data = 25 #number of measurement

udp_dao = udpy.UDP_DAO('127.0.0.1', 12346)

data_export = []
while len(data_export) < n_data:
    data = ast.literal_eval(udp_dao.readData())
    if data['major'] == 1 and data['minor'] == beacon:
        data['dist'] = dist
        data_export.append(data)
        print len(data_export)

#WRITE HEADER
if new_file == True:
    with open('eggs.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        header = []
        for h in data_export[0]:
            header.append(h)
        writer.writerow(header)
        for d in data_export:
            row = []
            for i in d:
                row.append(d[i])
            writer.writerow(row)
else:
    with open('eggs.csv', 'ab') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for d in data_export:
            row = []
            for i in d:
                row.append(d[i])
            writer.writerow(row)
